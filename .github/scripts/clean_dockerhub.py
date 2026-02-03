import requests
import os
import sys
from datetime import datetime, timedelta, timezone

USERNAME = os.getenv('DOCKERHUB_USERNAME')
PASSWORD = os.getenv('DOCKERHUB_PASSWORD')
ORG = os.getenv('DOCKERHUB_ORG')
REPO = os.getenv('DOCKERHUB_REPO')

def get_token():
    url = "https://hub.docker.com/v2/users/login/"
    r = requests.post(url, json={"username": USERNAME, "password": PASSWORD})
    if r.status_code != 200:
        sys.exit(1)
    return r.json().get("token")

def main():
    token = get_token()
    headers = {"Authorization": f"JWT {token}"}
    
    url = f"https://hub.docker.com/v2/repositories/{ORG}/{REPO}/images?page_size=100"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        sys.exit(1)
    
    images = r.json().get('results', [])
    now = datetime.now(timezone.utc)
    
    for img in images:
        digest = img.get('digest')
        tags = img.get('tags', [])
        last_pushed_str = img.get('last_pushed')
        size = img.get('size', 0) / (1024 * 1024)

        if not last_pushed_str:
            continue

        last_pushed = datetime.fromisoformat(last_pushed_str.replace('Z', '+00:00'))
        diff = (now - last_pushed).total_seconds()

        if not tags and diff > 120 and size > 1.0:
            del_url = f"https://hub.docker.com/v2/repositories/{ORG}/{REPO}/manifests/{digest}"
            requests.delete(del_url, headers=headers)

if __name__ == "__main__":
    main()