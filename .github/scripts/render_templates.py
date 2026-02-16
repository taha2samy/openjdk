import os
import re
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
VERSIONS_DIR = os.path.join(BASE_DIR, 'versions')
VERSIONS_HCL = os.path.join(BASE_DIR, 'versions.hcl')
BAKE_HCL = os.path.join(BASE_DIR, 'docker-bake.hcl')

TARGET_VERSIONS = ["8", "11", "17", "21", "25"]

def parse_hcl_to_dict(file_path):
    variables = {}
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found.")
        return variables

    with open(file_path, 'r') as f:
        content = f.read()

    flat_vars = re.findall(r'^(\w+)\s*=\s*"([^"]+)"', content, re.MULTILINE)
    for key, val in flat_vars:
        variables[key] = val

    bake_vars = re.findall(r'variable\s+"(\w+)"\s*{\s*default\s*=\s*"([^"]+)"', content)
    for key, val in bake_vars:
        variables[key] = val

    return variables

def main():
    config_data = {}
    config_data.update(parse_hcl_to_dict(VERSIONS_HCL))
    config_data.update(parse_hcl_to_dict(BAKE_HCL))

    print(f"Loaded {len(config_data)} variables from HCL files.")
    print(f"Base Digest: {config_data.get('WOLFI_BASE_DIGEST', 'N/A')}")
    print(f"Registry: {config_data.get('DOCKER_REGISTRY', 'N/A')}")

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    for version in TARGET_VERSIONS:
        version_str = str(version)
        output_path = os.path.join(VERSIONS_DIR, version_str)
        os.makedirs(output_path, exist_ok=True)

        context = config_data.copy()
        context.update({
            "version": version_str
        })

        print(f"--- Processing Java {version_str} ---")

        templates_to_render = [
            ("Dockerfile.j2", "Dockerfile"),
            ("build.hcl.j2", "build.hcl"),
            ("java.security.j2", "java.security")
        ]

        for tpl_name, out_name in templates_to_render:
            try:
                tpl = env.get_template(tpl_name)
                rendered_content = tpl.render(context)

                with open(os.path.join(output_path, out_name), "w") as f:
                    f.write(rendered_content)
                print(f"  [OK] {out_name}")
            except Exception as e:
                print(f"  [ERROR] Failed to render {tpl_name}: {e}")

if __name__ == "__main__":
    main()
