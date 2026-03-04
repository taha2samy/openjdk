#!/usr/bin/env python3

import json
import os
import shutil
import yaml
import logging
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("RENDERER")

RENDER_MAP = {
    "Dockerfile.j2": "Dockerfile",
    "java.security.j2": "java.security",
    "build.hcl.j2": "build.hcl"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(BASE_DIR, "config/context.json")
FLAVORS_FILE = os.path.join(BASE_DIR, "config/flavors.yml")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_ROOT = os.path.join(BASE_DIR, "versions")

def load_data():
    with open(CONTEXT_FILE, 'r') as f:
        context = json.load(f)
    with open(FLAVORS_FILE, 'r') as f:
        flavors = yaml.safe_load(f)
    return context, flavors




def render_all():
    context, flavors_cfg = load_data()
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    env.filters['setup_flavor'] = setup_flavor_filter

    source_packages = context.get("wolfi_packages", {})
    java_versions = context.get("java", {})
    image_flavors = flavors_cfg.get("image_flavors", {})

    for v_key, v_data in java_versions.items():
        v_output_dir = os.path.join(OUTPUT_ROOT, v_key)
        os.makedirs(v_output_dir, exist_ok=True)

        flat_vars = {}
        flat_vars.update(context.get('images', {}))
        flat_vars.update(source_packages) 
        flat_vars.update(v_data)
        
        for k, v in context.items():
            if k not in ['java', 'images', 'wolfi_packages']:
                flat_vars[k] = v

        resolved_flavors = {}
        for f_name, f_spec in image_flavors.items():
            flavor_pkgs = []
            for pkg in f_spec.get("packages", []):
                version = source_packages.get(pkg)
                if version:
                    flavor_pkgs.append(f"{pkg}={version}")
                else:
                    logger.warning(f"Package '{pkg}' skipped for flavor '{f_name}'")
            
            clean_name = f_name.replace("-", "_")
            resolved_flavors[clean_name] = {
                "name": f_name,
                "java_type": f_spec.get("java_type"),
                "options": f_spec.get("options", {}),
                "packages": flavor_pkgs
            }
        
        flat_vars["flavors"] = resolved_flavors

        for src_tpl, out_name in RENDER_MAP.items():
            try:
                template = env.get_template(src_tpl)
                content = template.render(**flat_vars)
                with open(os.path.join(v_output_dir, out_name.strip()), 'w') as f:
                    f.write(content)
            except Exception as e:
                logger.error(f"Failed to render {src_tpl}: {e}")
    logger.info(f"✅ Render complete for {len(java_versions)} versions.")
    
def setup_flavor_filter(f_id, flavors_dict):
    spec = flavors_dict.get(f_id)
    if not spec: return ""

    opt = spec.get('options', {})
    root = f"/rootfs/{f_id}"
    cache_path = "/var/cache/apk"
    
    unique_pkgs = list(dict.fromkeys(spec.get('packages', [])))
    pkgs_str = " ".join(unique_pkgs)

    prep_cmds = [f"mkdir -p {root}/etc/apk {root}/var/lib/apk"]
    if opt.get('has_package_manager'):
        prep_cmds.append(f"cp -a /etc/apk/repositories /etc/apk/keys {root}/etc/apk/")
    
    run_prep = f"RUN {' && '.join(prep_cmds)}"

    main_cmds = []
    main_cmds.append(
        f"apk add --initdb --no-scripts --root {root} "
        f"--cache-dir {cache_path} "
        f"--keys-dir /etc/apk/keys --repositories-file /etc/apk/repositories {pkgs_str}"
    )

    if opt.get('use_ldconfig'):
        main_cmds.append(f"ldconfig -r {root}")

    if opt.get('has_shell'):
        busybox_setup = (
            f"for a in $({root}/usr/bin/busybox --list); do "
            f"ln -sf busybox {root}/usr/bin/$a; done && "
            f"ln -sf busybox {root}/usr/bin/sh"
        )
        main_cmds.append(busybox_setup)

    cache_mount = f"--mount=type=cache,id=wolfi-apk,target={cache_path} " if opt.get('use_cache') else ""
    
    run_main = f"# kics-scan ignore-line\nRUN {cache_mount}{' && '.join(main_cmds)}"

    return f"{run_prep}\n{run_main}"

if __name__ == "__main__":
    if os.path.exists(OUTPUT_ROOT):
        shutil.rmtree(OUTPUT_ROOT)
    render_all()