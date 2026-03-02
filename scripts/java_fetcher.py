import requests
import logging
import sys
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def fetch_java_metadata(java_versions: list) -> dict:
    java_data = {}

    for version in java_versions:
        logger.info(f"Fetching metadata for Java {version} from Adoptium API...")

        url = f"https://api.adoptium.net/v3/assets/latest/{version}/hotspot"
        params = {
            "os": "linux",
            "vendor": "eclipse"
        }

        assets = None
        for attempt in range(3):
            try:
                response = requests.get(url, params=params, timeout=15)
                response.raise_for_status()
                assets = response.json()
                break
            except requests.exceptions.RequestException as e:
                if attempt < 2:
                    logger.warning(f"Attempt {attempt + 1} failed for Java {version}. Retrying in 10s... Error: {e}")
                    time.sleep(10)
                else:
                    logger.error(f"Final failure fetching Java {version}: {e}")
                    sys.exit(1)

        v_data = {
            "version": version
        }

        for asset in assets:
            binary = asset.get("binary", {})
            arch = binary.get("architecture")
            image_type = binary.get("image_type")

            if arch not in ["x64", "aarch64"] or image_type not in ["jdk", "jre"]:
                continue

            docker_arch = "amd64" if arch == "x64" else "arm64"
            prefix = f"{image_type}_{docker_arch}"
            package = binary.get("package", {})

            v_data[f"{prefix}_url"] = package.get("link")
            v_data[f"{prefix}_sha"] = package.get("checksum")
            v_data[f"{prefix}_binary_name"] = package.get("name")

            if "full_ver" not in v_data:
                ver_info = asset.get("version", {})
                v_data["full_ver"] = ver_info.get("openjdk_version")
                v_data["sec_level"] = str(ver_info.get("security", ""))
                v_data["semver"] = ver_info.get("semver")
                v_data["scm_ref"] = asset.get("scm_ref")
                v_data["upstream_update"] = binary.get("updated_at")

        required_keys = ["jdk_amd64_url", "jdk_arm64_url", "jre_amd64_url", "jre_arm64_url"]
        missing = [k for k in required_keys if k not in v_data]
        if missing:
            logger.warning(f"Java {version} is missing some artifacts: {missing}")

        java_data[version] = v_data
        logger.info(f"Successfully processed Java {version} ({v_data.get('full_ver')})")

    return java_data

if __name__ == "__main__":
    import json
    test_versions = ["8", "17", "21"]
    result = fetch_java_metadata(test_versions)
    print("\n--- JSON OUTPUT ---")
    print(json.dumps(result, indent=4))