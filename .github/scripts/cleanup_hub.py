import requests
import sys
import os

USERNAME = os.getenv('DOCKERHUB_USERNAME')
PASSWORD = os.getenv('DOCKERHUB_PASSWORD')
ORG = os.getenv('DOCKERHUB_ORG')
REPO = os.getenv('DOCKERHUB_REPO')
KEEP_LAST = int(os.getenv('KEEP_LAST', '10'))

BASE_V2_URL = os.getenv('DOCKER_BASE_URL', 'https://hub.docker.com/v2')
LOGIN_URL = os.getenv('DOCKER_LOGIN_URL', f"{BASE_V2_URL}/users/login/")
TAGS_URL = os.getenv('DOCKER_TAGS_URL', f"{BASE_V2_URL}/repositories/{ORG}/{REPO}/tags")

def check_env_vars():
    missing = []
    if not USERNAME: missing.append('DOCKERHUB_USERNAME')
    if not PASSWORD: missing.append('DOCKERHUB_PASSWORD')
    if not ORG and not os.getenv('DOCKER_TAGS_URL'): missing.append('DOCKERHUB_ORG')
    if not REPO and not os.getenv('DOCKER_TAGS_URL'): missing.append('DOCKERHUB_REPO')
    
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

def get_token():
    print(f"Logging in to: {LOGIN_URL}")
    response = requests.post(LOGIN_URL, json={"username": USERNAME, "password": PASSWORD})
    if response.status_code != 200:
        print(f"Error logging in: {response.status_code} - {response.text}")
        sys.exit(1)
    return response.json()["token"]

def get_tags(token):
    headers = {"Authorization": f"JWT {token}"}
    tags = []
    url = f"{TAGS_URL}?page_size=100"
    
    print(f"Fetching tags from: {TAGS_URL}")
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching tags: {response.text}")
            break
        
        data = response.json()
        tags.extend(data['results'])
        url = data.get('next')
        
    return tags

def is_safe_to_delete(tag_name):
    if tag_name == "latest":
        return False
    if (tag_name.startswith("sha256-") or 
        tag_name.endswith(".att") or 
        tag_name.endswith(".sig") or 
        tag_name.endswith(".sbom")):
        return False
    return True

def delete_tag(token, tag_name):
    url = f"{TAGS_URL}/{tag_name}"
    headers = {"Authorization": f"JWT {token}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Deleted: {tag_name}")
    else:
        print(f"Failed to delete {tag_name}: {response.text}")

def main():
    check_env_vars()
    print(f"Starting Cleanup for {ORG}/{REPO}")
    
    token = get_token()
    all_tags = get_tags(token)
    
    all_tags.sort(key=lambda x: x['last_updated'], reverse=True)
    image_tags = [t for t in all_tags if is_safe_to_delete(t['name'])]
    
    print(f"Total tags: {len(all_tags)}")
    print(f"Actual Image tags (cleanable): {len(image_tags)}")

    if len(image_tags) <= KEEP_LAST:
        print(f"Count ({len(image_tags)}) is <= Limit ({KEEP_LAST}). No cleanup needed.")
        return

    tags_to_delete = image_tags[KEEP_LAST:]
    print(f"Keeping latest {KEEP_LAST}. Deleting {len(tags_to_delete)} old images...")
    
    for tag in tags_to_delete:
        delete_tag(token, tag['name'])

if __name__ == "__main__":
    main()
