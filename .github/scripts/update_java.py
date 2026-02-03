import requests
import json
import os
from datetime import datetime

JAVA_VERSIONS = [8, 11, 17, 21, 25]
IMAGE_TYPES = ["jdk", "jre"]
ARCHITECTURES = {
    "amd64": "x64",
    "arm64": "aarch64"
}
ADOPTIUM_API_BASE = "https://api.adoptium.net/v3/assets/latest"
WOLFI_IMAGES = {
    "base": "cgr.dev/chainguard/wolfi-base",
    "static": "cgr.dev/chainguard/static"
}
DB_FILE = "versions.json"

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
        headers = {
            "Accept": "application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.oci.image.index.v1+json"
        }
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
        "image_type": image_type,
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
            "url": pkg['link'],
            "sha": pkg['checksum'],
            "checksum_link": pkg.get('checksum_link'),
            "binary_name": pkg.get('name'),
            "openjdk_version": ver.get('openjdk_version'),
            "semver": ver.get('semver'),
            "major": ver.get('major'),
            "security_level": ver.get('security'),
            "build_number": ver.get('build'),
            "scm_ref": binary.get('scm_ref'),
            "updated_at": binary.get('updated_at'),
            "release_link": item.get('release_link'),
            "release_name": item.get('release_name'),
            "vendor": item.get('vendor'),
            "image_type": image_type,
            "workflow_run_id": os.getenv("GITHUB_RUN_ID", "none"),
            "workflow_name": os.getenv("GITHUB_WORKFLOW", "none")
        }
    except:
        return None

def main():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                current_data = json.load(f)
        except:
            current_data = {}
    else:
        current_data = {}

    new_data = {}
    has_changes = False

    for v in JAVA_VERSIONS:
        ver_key = f"java{v}"
        new_data[ver_key] = {}
        for img_type in IMAGE_TYPES:
            new_data[ver_key][img_type] = {}
            for arch_id, api_arch in ARCHITECTURES.items():
                result = fetch_java_metadata(v, api_arch, img_type)
                if result:
                    new_data[ver_key][img_type][arch_id] = result
                    old_sha = current_data.get(ver_key, {}).get(img_type, {}).get(arch_id, {}).get("sha")
                    if result["sha"] != old_sha:
                        has_changes = True
                else:
                    if ver_key in current_data and img_type in current_data[ver_key] and arch_id in current_data[ver_key][img_type]:
                        new_data[ver_key][img_type][arch_id] = current_data[ver_key][img_type][arch_id]

    new_data["wolfi"] = {}
    for wolfi_type, image_name in WOLFI_IMAGES.items():
        digest = fetch_image_digest(image_name, "latest")
        if digest:
            wolfi_entry = {
                "image": image_name,
                "tag": "latest",
                "digest": digest,
                "workflow_run_id": os.getenv("GITHUB_RUN_ID", "none")
            }
            new_data["wolfi"][wolfi_type] = wolfi_entry
            old_digest = current_data.get("wolfi", {}).get(wolfi_type, {}).get("digest")
            if digest != old_digest:
                has_changes = True
        else:
            if "wolfi" in current_data and wolfi_type in current_data["wolfi"]:
                new_data["wolfi"][wolfi_type] = current_data["wolfi"][wolfi_type]

    if has_changes:
        with open(DB_FILE, "w") as f:
            json.dump(new_data, f, indent=4)
        print("Update_Found")
    else:
        print("No_Changes")

if __name__ == "__main__":
    main()