import subprocess
import logging
import sys
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def run_with_retry(cmd, retries=3, delay=10):
    for i in range(retries):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            if i == retries - 1: raise e
            logger.warning(f"Attempt {i+1} failed, retrying in {delay}s...")
            time.sleep(delay)

def fetch_images_metadata(images_list):
    resolved = {}
    for img in images_list:
        img_key = img.split("/")[-1].split(":")[0].replace("-", "_")
        logger.info(f"Resolving: {img}")
        
        try:
            run_with_retry(["docker", "pull", "-q", img])
            inspect_cmd = ["docker", "inspect", "--format={{index .RepoDigests 0}}", img]
            repo_digest = subprocess.run(inspect_cmd, capture_output=True, text=True, check=True).stdout.strip()
            
            sha = repo_digest.split("@")[1] if "@" in repo_digest else repo_digest
            resolved[img_key] = f"{img.split(':')[0]}@{sha}"
            logger.info(f" -> Found: {sha[:12]}")
        except Exception as e:
            logger.error(f"Failed to resolve {img} after retries")
            sys.exit(1)
    return resolved