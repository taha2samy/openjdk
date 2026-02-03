import requests, os, json, sys

USERNAME = os.getenv('DOCKERHUB_USERNAME')
PASSWORD = os.getenv('DOCKERHUB_PASSWORD')
ORG = os.getenv('DOCKERHUB_ORG')
REPO = os.getenv('DOCKERHUB_REPO')

def main():
    r = requests.post("https://hub.docker.com/v2/users/login/", json={"username": USERNAME, "password": PASSWORD})
    if r.status_code != 200:
        print(f"Error Login: {r.status_code} {r.text}")
        sys.exit(1)
    
    token = r.json().get("token")
    headers = {"Authorization": f"JWT {token}"}
    
    digests = []
    url = f"https://hub.docker.com/v2/repositories/{ORG}/{REPO}/images?page_size=10000"
    
    while url:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Error Fetch: {res.status_code} {res.text}")
            sys.exit(1)
        data = res.json()
        digests.extend([img['digest'] for img in data.get('results', [])])
        url = data.get('next')
        
    with open("old_digests.json", "w") as f:
        json.dump(digests, f)
    print(f"Recorded {len(digests)} digests")

if __name__ == "__main__":
    main()