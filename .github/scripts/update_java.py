import requests
import json
import os
from datetime import datetime

JAVA_VERSIONS = [8, 11, 17, 21, 25]
ARCHITECTURES = {
    "amd64": "x64",
    "arm64": "aarch64"
}
DB_FILE = "versions.json"
ADOPTIUM_API_BASE = "https://api.adoptium.net/v3/assets/latest"

def fetch_java_metadata(major_version, arch):
    url = f"{ADOPTIUM_API_BASE}/{major_version}/hotspot"
    params = {
        "architecture": arch,
        "image_type": "jdk",
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
            "workflow_run_id": os.getenv("GITHUB_RUN_ID", "local-manual-run"),
            "workflow_name": os.getenv("GITHUB_WORKFLOW", "manual-execution"),
        }
    except Exception:
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
        
        for arch_id, api_arch in ARCHITECTURES.items():
            result = fetch_java_metadata(v, api_arch)
            if result:
                new_data[ver_key][arch_id] = result
                
                old_sha = current_data.get(ver_key, {}).get(arch_id, {}).get("sha")
                if result["sha"] != old_sha:
                    has_changes = True

    if has_changes:
        with open(DB_FILE, "w") as f:
            json.dump(new_data, f, indent=4)
        print("Update_Found")
    else:
        print("No_Changes")

if __name__ == "__main__":
    main()