import os
import yaml
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("FLAVOR_RESOLVER")

def resolve_flavor_specs(flavors_config: dict, context_data: dict) -> dict:
    """
    Maps flavor package requests to resolved versions found in context.json 
    and consolidates build options for the rendering engine.
    """
    resolved_flavors = {}
    
    source_packages = context_data.get("wolfi_packages", {})
    flavors_definitions = flavors_config.get("image_flavors", {})

    for name, spec in flavors_definitions.items():
        logger.info(f"Resolving specs for flavor: {name}")
        
        flavor_data = {
            "java_type": spec.get("java_type", "jre"),
            "options": spec.get("options", {}),
            "packages": []
        }

        requested_packages = spec.get("packages", [])

        for pkg in requested_packages:
            if pkg in source_packages:
                version = source_packages[pkg]
                # Format: package=version
                flavor_data["packages"].append(f"{pkg}={version}")
            else:
                raise ValueError(f"Flavor '{name}' requires '{pkg}' but it is missing from context.json")

        resolved_flavors[name] = flavor_data

    return resolved_flavors

if __name__ == "__main__":
    # Mock data to simulate config/ directory contents
    mock_flavors_yml = {
        "image_flavors": {
            "jre-distroless": {
                "java_type": "jre",
                "options": {"has_shell": False},
                "packages": ["glibc", "zlib", "libstdc++"]
            },
            "jre-standard": {
                "java_type": "jre",
                "options": {"has_shell": True},
                "packages": ["glibc", "zlib", "libstdc++", "busybox"]
            },
            "jdk-devel": {
                "java_type": "jdk",
                "options": {"has_shell": True},
                "packages": ["glibc", "zlib", "libstdc++", "busybox", "bash", "curl"]
            }
        }
    }

    mock_context_json = {
        "wolfi_packages": {
            "glibc": "2.40-r1",
            "zlib": "1.3.1-r0",
            "libstdc++": "13.2-r1",
            "busybox": "1.36-r5",
            "bash": "5.2-r0",
            "curl": "8.5.0-r0"
        }
    }

    print("--- STARTING FLAVOR RESOLUTION TEST ---")
    try:
        # Simulate resolving logic
        final_specs = resolve_flavor_specs(mock_flavors_yml, mock_context_json)
        
        # Display formatted output
        print(json.dumps(final_specs, indent=4))
        
        print("\n--- TEST PASSED: Flavors resolved and version-pinned successfully ---")
    except Exception as e:
        print(f"\n--- TEST FAILED: {str(e)} ---")