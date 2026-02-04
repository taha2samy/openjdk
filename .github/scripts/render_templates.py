import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
VERSIONS_DIR = os.path.join(BASE_DIR, 'versions')
HCL_FILE = os.path.join(BASE_DIR, 'versions.hcl')

TARGET_VERSIONS = ["8", "11", "17", "21", "25"]

def parse_hcl_vars(file_path):
    """Simple parser to extract variable values from versions.hcl"""
    variables = {}
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return variables

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')
                variables[key] = value
    return variables

def main():
    hcl_vars = parse_hcl_vars(HCL_FILE)
    
    wolfi_base = hcl_vars.get("WOLFI_BASE_DIGEST", "latest")
    wolfi_static = hcl_vars.get("WOLFI_STATIC_DIGEST", "latest")

    print(f"Loaded Wolfi Base: {wolfi_base}")
    print(f"Loaded Wolfi Static: {wolfi_static}")

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    for version in TARGET_VERSIONS:
        version_str = str(version)
        output_path = os.path.join(VERSIONS_DIR, version_str)
        os.makedirs(output_path, exist_ok=True)

        context = {
            "version": version_str,
            "WOLFI_BASE_DIGEST": wolfi_base,
            "WOLFI_STATIC_DIGEST": wolfi_static
        }

        print(f"Generating files for Java {version_str}...")

        try:
            docker_tpl = env.get_template("Dockerfile.j2")
            with open(os.path.join(output_path, "Dockerfile"), "w") as f:
                f.write(docker_tpl.render(context))
        except Exception as e:
            print(f"Error rendering Dockerfile for {version_str}: {e}")

        try:
            build_tpl = env.get_template("build.hcl.j2")
            with open(os.path.join(output_path, "build.hcl"), "w") as f:
                f.write(build_tpl.render(context))
        except Exception as e:
            print(f"Error rendering build.hcl for {version_str}: {e}")

if __name__ == "__main__":
    main()