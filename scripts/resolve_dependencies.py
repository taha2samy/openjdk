#!/usr/bin/env python3

import yaml
import json
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_fetcher import fetch_images_metadata
from java_fetcher import fetch_java_metadata
from package_fetcher import fetch_package_versions

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("RESOLVER")

CONFIG_FILE = "config/requirements.yml"
OUTPUT_FILE = "config/context.json"

def main():
    if not os.path.exists(CONFIG_FILE):
        logger.error(f"Config file not found: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)

    final_context = {}
    runner_image = "cgr.dev/chainguard/wolfi-base:latest"

    if "images" in config:
        logger.info("Resolving Docker Images...")
        resolved_images = fetch_images_metadata(config["images"])
        final_context["images"] = resolved_images

        for key, ref in resolved_images.items():
            if "wolfi" in key or "base" in key:
                runner_image = ref
                break

    if "java_versions" in config:
        logger.info("Resolving Java Versions...")
        final_context["java"] = fetch_java_metadata(config["java_versions"])

    if "wolfi_packages" in config:
        logger.info(f"Resolving OS Packages using runner: {runner_image}...")
        final_context["wolfi_packages"] = fetch_package_versions(runner_image, config["wolfi_packages"])

    KNOWN_KEYS = ["images", "java_versions", "wolfi_packages"]

    for key, value in config.items():
        if key not in KNOWN_KEYS:
            logger.info(f"Passing through custom config: '{key}'")
            final_context[key] = value

    logger.info(f"Writing final context to {OUTPUT_FILE}...")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(final_context, f, indent=4, sort_keys=True)

    logger.info("Dependency resolution complete!")

if __name__ == "__main__":
    main()