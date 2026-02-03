import requests, os, json, sys

USERNAME = os.getenv('DOCKERHUB_USERNAME')
PASSWORD = os.getenv('DOCKERHUB_PASSWORD')
ORG = os.getenv('DOCKERHUB_ORG')
REPO = os.getenv('DOCKERHUB_REPO')

def main():
    if not os.path.exists("old_digests.json"):
        sys.exit(0)
        
    with open("old_digests.json", "r") as f:
        old_digests = json.load(f)

    login_url = "https://hub.docker.com/v2/users/login/"
    r = requests.post(login_url, json={"username": USERNAME, "password": PASSWORD})
    if r.status_code != 200:
        sys.exit(1)
        
    token = r.json().get("token")
    headers = {"Authorization": f"JWT {token}"}

    images_url = f"https://hub.docker.com/v2/repositories/{ORG}/{REPO}/images"
    res = requests.get(images_url, headers=headers)
    if res.status_code != 200:
        sys.exit(1)
        
    current_images = res.json().get('results', [])

    for img in current_images:
        digest = img.get('digest')
        tags = img.get('tags', [])
        size = img.get('size', 0) / (1024 * 1024)

        if digest in old_digests and not tags and size > 1.0:
            del_url = f"https://hub.docker.com/v2/repositories/{ORG}/{REPO}/manifests/{digest}"
            requests.delete(del_url, headers=headers)

if __name__ == "__main__":
    main()