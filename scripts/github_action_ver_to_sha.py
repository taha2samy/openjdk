import os
import re
import subprocess
from ruamel.yaml import YAML

def is_sha(text):
    """Checks if a string is a 40-character git SHA."""
    return bool(re.match(r'^[a-fA-F0-9]{40}$', text))

def get_sha(repo, tag):
    """Fetches the full commit SHA for a given repo and tag/branch using the gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}/commits/{tag}", "--jq", ".sha"],
            capture_output=True,
            text=True,
            check=True
        )
        sha = result.stdout.strip()
        return sha if is_sha(sha) else None
    except subprocess.CalledProcessError:
        print(f"   [!] Failed to fetch SHA for {repo}@{tag}")
        return None

def process_steps(steps):
    """
    Processes a list of steps, finds actions with versions, and pins them to a commit SHA.
    Adds the original version as a comment.
    """
    updated = False
    if not steps or not isinstance(steps, list):
        return False

    for step in steps:
        uses = step.get('uses')
        # Skip local actions or actions without a version specifier
        if not uses or '@' not in uses or uses.startswith('./'):
            continue
        
        repo, version = uses.split('@', 1)
        
        # Skip if the version is already a full SHA
        if is_sha(version):
            continue
        
        print(f"   [*] Pinning action: {uses}")
        new_sha = get_sha(repo, version)
        
        if new_sha:
            # Update the 'uses' value to the full SHA
            step['uses'] = f"{repo}@{new_sha}"
            
            # Add the original version as an end-of-line comment
            step.yaml_add_eol_comment(f"{version}", key='uses')
            
            print(f"   [+] Pinned: {uses} -> {new_sha[:7]}")
            updated = True
            
    return updated

def pin_files(file_path):
    """Loads a YAML file, processes its steps, and writes it back if updated."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"\n--- Processing: {file_path} ---")
    yaml = YAML()
    yaml.preserve_quotes = True
    # Standard YAML indentation for GitHub Actions
    yaml.indent(mapping=2, sequence=4, offset=2)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f)

    file_updated = False

    # Standard workflow structure: jobs -> <job_name> -> steps
    if 'jobs' in data:
        for job_name, job_data in data['jobs'].items():
            if isinstance(job_data, dict) and 'steps' in job_data:
                if process_steps(job_data['steps']):
                    file_updated = True
    
    # Composite action structure: runs -> steps
    elif 'runs' in data and 'steps' in data['runs']:
        if process_steps(data['runs']['steps']):
            file_updated = True

    if file_updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
        print(f"Done! {file_path} updated.")
    else:
        print(f"No changes needed for {file_path}.")

if __name__ == "__main__":
    # Add all your workflow or action files here
    files_to_pin = [
        ".github/workflows/build-images.yml",
        # ".github/workflows/another-workflow.yml"
    ]
    
    for file in files_to_pin:
        pin_files(file)