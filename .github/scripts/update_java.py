import requests
import json
import os
from datetime import datetime

JAVA_VERSIONS = [8, 11, 17, 21, 25]
IMAGE_TYPES = ["JDK", "JRE"]
ARCHITECTURES = {
    "AMD64": "x64",
    "ARM64": "aarch64"
}
ADOPTIUM_API_BASE = "https://api.adoptium.net/v3/assets/latest"
WOLFI_IMAGES = {
    "BASE": "cgr.dev/chainguard/wolfi-base",
    "STATIC": "cgr.dev/chainguard/static"
}
HCL_FILE = "versions.hcl"

def get_docker_token(registry, repository):
    auth_url = f"https://{registry}/token?service={registry}&scope=repository:{repository}:pull"
    try:
        r = requests.get(auth_url, timeout=10)
        if r.status_code == 200:
            return r.json().get("token")
    except:
        pass
    return None

def fetch_image_digest(full_image_name, tag="latest"):
    try:
        parts = full_image_name.split('/', 1)
        if len(parts) == 2:
            registry, repository = parts
        else:
            registry = "registry-1.docker.io"
            repository = parts[0]
            if '/' not in repository:
                repository = f"library/{repository}"

        manifest_url = f"https://{registry}/v2/{repository}/manifests/{tag}"
        headers = {"Accept": "application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.oci.image.index.v1+json"}
        response = requests.head(manifest_url, headers=headers, timeout=10)

        if response.status_code == 401:
            token = get_docker_token(registry, repository)
            if token:
                headers["Authorization"] = f"Bearer {token}"
                response = requests.head(manifest_url, headers=headers, timeout=10)

        response.raise_for_status()
        return response.headers.get("Docker-Content-Digest")
    except:
        return None

def fetch_java_metadata(major_version, arch, image_type):
    url = f"{ADOPTIUM_API_BASE}/{major_version}/hotspot"
    params = {
        "architecture": arch,
        "image_type": image_type.lower(),
        "os": "linux",
        "vendor": "eclipse"
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        if not data:
            return None
            
        item = data[0]
        binary = item['binary']
        pkg = binary['package']
        ver = item['version']
        
        return {
            "URL": pkg['link'],
            "SHA": pkg['checksum'],
            "CHECKSUM_LINK": pkg.get('checksum_link'),
            "BINARY_NAME": pkg.get('name'),
            "FULL_VER": ver.get('openjdk_version'),
            "SEMVER": ver.get('semver'),
            "MAJOR": ver.get('major'),
            "SEC_LEVEL": ver.get('security'),
            "BUILD_NUMBER": ver.get('build'),
            "SCM_REF": binary.get('scm_ref'),
            "UPSTREAM_UPDATE": binary.get('updated_at'),
            "RELEASE_LINK": item.get('release_link'),
            "RELEASE_NAME": item.get('release_name'),
            "VENDOR": item.get('vendor'),
            "WORKFLOW_RUN_ID": os.getenv("GITHUB_RUN_ID", "none"),
            "WORKFLOW_NAME": os.getenv("GITHUB_WORKFLOW", "none")
        }
    except:
        return None

def main():
    hcl_lines = []
    
    for w_name, img_path in WOLFI_IMAGES.items():
        digest = fetch_image_digest(img_path)
        if digest:
            hcl_lines.append(f'WOLFI_{w_name}_DIGEST = "{digest}"')

    for v in JAVA_VERSIONS:
        for itype in IMAGE_TYPES:
            for arch_label, api_arch in ARCHITECTURES.items():
                res = fetch_java_metadata(v, api_arch, itype)
                if res:
                    prefix = f"JAVA{v}_{itype}_{arch_label}"
                    for key, value in res.items():
                        hcl_lines.append(f'{prefix}_{key} = "{value}"')
                    
                    if itype == "JDK" and arch_label == "AMD64":
                        hcl_lines.append(f'JAVA{v}_FULL_VER = "{res["FULL_VER"]}"')
                        hcl_lines.append(f'JAVA{v}_SEC_LEVEL = "{res["SEC_LEVEL"]}"')
                        hcl_lines.append(f'JAVA{v}_SEMVER = "{res["SEMVER"]}"')
                        hcl_lines.append(f'JAVA{v}_SCM_REF = "{res["SCM_REF"]}"')
                        hcl_lines.append(f'JAVA{v}_UPSTREAM_UPDATE = "{res["UPSTREAM_UPDATE"]}"')

    new_hcl_content = "\n".join(hcl_lines)
    
    old_hcl_content = ""
    if os.path.exists(HCL_FILE):
        with open(HCL_FILE, "r") as f:
            old_hcl_content = f.read()

    if new_hcl_content.strip() != old_hcl_content.strip():
        with open(HCL_FILE, "w") as f:
            f.write(new_hcl_content)
        print("Update_Found")
    else:
        print("No_Changes")

if __name__ == "__main__":
    main()