import subprocess
import logging
import sys
import time
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def fetch_package_versions(runner_image, packages):
    if not packages: return {}
    
    logger.info(f"Fetching packages from: {runner_image}")
    pkgs_str = " ".join(packages)
    script = f"apk update > /dev/null && apk search -x {pkgs_str}"

    for i in range(3):
        try:
            res = subprocess.run(
                ["docker", "run", "--rm", runner_image, "sh", "-c", script],
                capture_output=True, text=True, check=True, timeout=180
            )
            
            versions = {}
            lines = res.stdout.strip().split("\n")
            for line in lines:
                line = line.strip()
                if not line: continue
                
                for p in packages:
                    prefix = f"{p}-"
                    if line.startswith(prefix):
                        v_candidate = line[len(prefix):]
                        if v_candidate and v_candidate[0].isdigit():
                            versions[p] = v_candidate
                            break
            
            missing = set(packages) - set(versions.keys())
            if missing:
                logger.warning(f"Missing packages: {missing}")
                
            return versions
        except Exception as e:
            if i == 2:
                logger.error(f"Final failure fetching packages: {e}")
                sys.exit(1)
            logger.warning(f"Package fetch attempt {i+1} failed, retrying...")
            time.sleep(5)

if __name__ == "__main__":
    TEST_IMAGE = "cgr.dev/chainguard/wolfi-base:latest"
    TEST_PKGS = ["glibc", "busybox", "zlib", "ca-certificates"]
    
    print(f"--- STARTING TEST ON {TEST_IMAGE} ---")
    try:
        results = fetch_package_versions(TEST_IMAGE, TEST_PKGS)
        print(json.dumps(results, indent=4))
        
        if "busybox" in results and "full" in results["busybox"]:
            print("TEST FAILED: detected 'full' in version string")
        else:
            print("TEST PASSED: version string looks correct")
            
    except Exception as e:
        print(f"TEST CRASHED: {e}")