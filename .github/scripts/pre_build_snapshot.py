import requests, os, json, sys

USERNAME = os.getenv('DOCKERHUB_USERNAME')
PASSWORD = os.getenv('DOCKERHUB_PASSWORD')
ORG = os.getenv('DOCKERHUB_ORG')
REPO = os.getenv('DOCKERHUB_REPO')

def main():
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
        
    digests = [img['digest'] for img in res.json().get('results', [])]
    
    with open("old_digests.json", "w") as f:
        json.dump(digests, f)

if __name__ == "__main__":
    main()