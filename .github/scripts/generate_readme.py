import json
import subprocess
import argparse
import os
import sys
from jinja2 import Template

def format_size(size_bytes):
    """تحويل الحجم بالبايتات إلى وحدة مناسبة"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def get_image_size_from_docker_manifest(image_tag, arch):
    """
    جلب حجم الـ image من Docker manifest مباشرة
    """
    try:
        # تشغيل docker manifest inspect
        cmd = f"docker manifest inspect --verbose {image_tag}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"⚠️  Warning: Failed to inspect {image_tag}: {result.stderr}", file=sys.stderr)
            return "N/A", "N/A"
        
        # Parse JSON
        manifests = json.loads(result.stdout)
        
        # البحث عن الـ manifest المطلوب
        for manifest in manifests:
            descriptor = manifest.get("Descriptor", {})
            platform = descriptor.get("platform", {})
            
            if platform.get("architecture") == arch and platform.get("os") == "linux":
                # استخراج OCIManifest
                oci_manifest = manifest.get("OCIManifest", {})
                if not oci_manifest:
                    continue
                
                # حساب الحجم
                total_size = 0
                
                # إضافة حجم الـ layers
                layers = oci_manifest.get("layers", [])
                for layer in layers:
                    total_size += layer.get("size", 0)
                
                # إضافة حجم الـ config
                config = oci_manifest.get("config", {})
                total_size += config.get("size", 0)
                
                # الـ digest
                digest = descriptor.get("digest", "")
                
                return format_size(total_size), digest
        
        print(f"⚠️  Warning: No manifest found for {arch} in {image_tag}", file=sys.stderr)
        return "N/A", "N/A"
        
    except Exception as e:
        print(f"❌ Error getting image size for {image_tag}/{arch}: {e}", file=sys.stderr)
        return "N/A", "N/A"

def extract_artifact_links(metadata, target_key, image_tag, run_id=None):
    """
    استخراج روابط الـ artifacts (SBOM, provenance, attestations) من metadata
    """
    artifacts = {
        'sbom': None,
        'provenance': None,
        'attestation': None,
        'cosign_sbom': None,
        'cosign_provenance': None
    }
    
    if target_key not in metadata:
        return artifacts
    
    target_metadata = metadata[target_key]
    image_name = image_tag.split(':')[0] if image_tag else None
    digest = target_metadata.get('containerimage.digest', '')
    
    if not image_name or not digest:
        return artifacts
    
    # استخراج org و repo من image name
    # مثال: ghcr.io/taha2samy/java -> owner=taha2samy, repo=java
    if 'ghcr.io' in image_name:
        parts = image_name.replace('ghcr.io/', '').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1]
            
            # GitHub Attestations API URLs
            # https://github.com/{owner}/{package}/attestations/{digest}
            base_attestation_url = f"https://github.com/{owner}/{repo}/attestations"
            
            # روابط الـ attestations على GitHub
            artifacts['sbom'] = f"{base_attestation_url}/{digest.replace('sha256:', '')}"
            artifacts['provenance'] = f"{base_attestation_url}/{digest.replace('sha256:', '')}"
            artifacts['attestation'] = f"{base_attestation_url}/{digest.replace('sha256:', '')}"
            
            # روابط Cosign للتحميل المباشر
            artifacts['cosign_sbom'] = f"{image_name}@{digest}"
            artifacts['cosign_provenance'] = f"{image_name}@{digest}"
    
    # إذا كان في run_id، نضيف رابط الـ GitHub Actions artifacts
    if run_id:
        artifacts['github_actions'] = f"https://github.com/{owner}/{repo}/actions/runs/{run_id}"
    
    return artifacts

def main():
    parser = argparse.ArgumentParser(description='Generate README from Docker images')
    parser.add_argument('--metadata', required=True, help='Path to metadata JSON file')
    parser.add_argument('--template', required=True, help='Path to Jinja2 template file')
    parser.add_argument('--version', required=True, help='Java version (e.g., 11, 17, 21)')
    parser.add_argument('--output', required=True, help='Output path for generated README')
    args_cli = parser.parse_args()

    # قراءة ملف الـ metadata
    try:
        with open(args_cli.metadata, 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Metadata file not found: {args_cli.metadata}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in metadata file: {e}", file=sys.stderr)
        sys.exit(1)

    v = args_cli.version
    
    # تحديد الـ targets
    targets = {
        'jdk': f"java{v}-jdk-std",
        'jre': f"java{v}-jre-std",
        'dist': f"java{v}-jre-distroless"
    }

    def get_image_tags(target_key):
        """استخراج جميع tags من metadata (GHCR و DockerHub)"""
        if target_key not in metadata:
            return {'ghcr': None, 'dockerhub': None}
        
        image_names = metadata[target_key].get("image.name", "")
        names = [name.strip() for name in image_names.split(',')]
        
        ghcr = next((n for n in names if 'ghcr.io' in n), None)
        dockerhub = next((n for n in names if 'ghcr.io' not in n and n), None)
        
        return {'ghcr': ghcr, 'dockerhub': dockerhub}

    # جلب tags
    image_tags = {k: get_image_tags(tk) for k, tk in targets.items()}

    # جلب بيانات provenance
    try:
        prov = metadata[targets['jdk']]["buildx.build.provenance/linux/amd64"]
        build_args = prov["invocation"]["parameters"]["args"]
        builder_id = prov["builder"]["id"]
        run_id = builder_id.split('/')[-3] if '/' in builder_id else None
    except KeyError as e:
        print(f"❌ Error: Missing key in metadata: {e}", file=sys.stderr)
        sys.exit(1)

    print("🔍 Fetching image details from manifests...")
    
    # جلب الأحجام والـ digests لكل variant وكل architecture
    variants = {}
    for variant_key, variant_name in [('jdk', 'JDK Standard'), 
                                       ('jre', 'JRE Standard'), 
                                       ('dist', 'JRE Distroless')]:
        
        ghcr_tag = image_tags[variant_key]['ghcr']
        dockerhub_tag = image_tags[variant_key]['dockerhub']
        
        # نستخدم GHCR كـ primary source
        primary_tag = ghcr_tag or dockerhub_tag
        
        if primary_tag:
            print(f"  📦 Processing {variant_name}...")
            amd_size, amd_digest = get_image_size_from_docker_manifest(primary_tag, "amd64")
            arm_size, arm_digest = get_image_size_from_docker_manifest(primary_tag, "arm64")
            
            # جلب artifact links
            artifacts = extract_artifact_links(metadata, targets[variant_key], primary_tag, run_id)
            
            variants[variant_key] = {
                'amd64': {'size': amd_size, 'digest': amd_digest},
                'arm64': {'size': arm_size, 'digest': arm_digest},
                'ghcr_tag': ghcr_tag,
                'dockerhub_tag': dockerhub_tag,
                'artifacts': artifacts
            }
        else:
            print(f"  ⚠️  Warning: No tags found for {variant_name}")
            variants[variant_key] = {
                'amd64': {'size': 'N/A', 'digest': 'N/A'},
                'arm64': {'size': 'N/A', 'digest': 'N/A'},
                'ghcr_tag': None,
                'dockerhub_tag': None,
                'artifacts': {'sbom': None, 'provenance': None, 'attestation': None}
            }

    # بناء الـ full SHA references
    def build_full_sha(tag, digest):
        if not tag or digest == "N/A":
            return "N/A"
        image_name = tag.split(':')[0]
        return f"`{image_name}@{digest}`"

    # تجهيز الـ context للـ template
    context = {
        # معلومات عامة
        "full_version": build_args.get("build-arg:JAVA_FULL_VERSION", "N/A"),
        "Version": build_args.get("build-arg:JAVA_VER", v),
        "build_date": build_args.get("build-arg:JAVA_UPSTREAM_UPDATE", "").split('T')[0],
        "upstream_date": build_args.get("build-arg:JAVA_UPSTREAM_UPDATE", "").split('T')[0],
        "build_proof": builder_id,
        "sbom": f"https://github.com/taha2samy/openjdk/actions/runs/{run_id}" if run_id else "N/A",
        "docker_pulls": "https://img.shields.io/docker/pulls/taha2samy/java?style=flat&logo=docker",
        "docker_pulls_url": "https://hub.docker.com/r/taha2samy/java",
        "vulnerability_scan_badge": "https://github.com/taha2samy/openjdk/actions/workflows/build-images.yml/badge.svg",
        
        # JDK Standard
        "amd64_jdk_size": variants['jdk']['amd64']['size'],
        "arm64_jdk_size": variants['jdk']['arm64']['size'],
        "amd64_jdk_full_sha": build_full_sha(variants['jdk']['ghcr_tag'], variants['jdk']['amd64']['digest']),
        "arm64_jdk_full_sha": build_full_sha(variants['jdk']['ghcr_tag'], variants['jdk']['arm64']['digest']),
        "amd64_jdk_digest": f"`{metadata[targets['jdk']].get('containerimage.digest', 'N/A')}`",
        "jdk_sbom_url": variants['jdk']['artifacts']['sbom'] if variants['jdk']['artifacts']['sbom'] else "N/A",
        "jdk_provenance_url": variants['jdk']['artifacts']['provenance'] if variants['jdk']['artifacts']['provenance'] else "N/A",
        "jdk_attestation_url": variants['jdk']['artifacts']['attestation'] if variants['jdk']['artifacts']['attestation'] else "N/A",
        "jdk_cosign_sbom": variants['jdk']['artifacts']['cosign_sbom'] if variants['jdk']['artifacts']['cosign_sbom'] else "N/A",
        
        # JRE Standard
        "amd64_jre_size": variants['jre']['amd64']['size'],
        "arm64_jre_size": variants['jre']['arm64']['size'],
        "amd64_jre_full_sha": build_full_sha(variants['jre']['ghcr_tag'], variants['jre']['amd64']['digest']),
        "arm64_jre_full_sha": build_full_sha(variants['jre']['ghcr_tag'], variants['jre']['arm64']['digest']),
        "amd64_jre_digest": f"`{metadata[targets['jre']].get('containerimage.digest', 'N/A')}`",
        "jre_sbom_url": variants['jre']['artifacts']['sbom'] if variants['jre']['artifacts']['sbom'] else "N/A",
        "jre_provenance_url": variants['jre']['artifacts']['provenance'] if variants['jre']['artifacts']['provenance'] else "N/A",
        "jre_attestation_url": variants['jre']['artifacts']['attestation'] if variants['jre']['artifacts']['attestation'] else "N/A",
        "jre_cosign_sbom": variants['jre']['artifacts']['cosign_sbom'] if variants['jre']['artifacts']['cosign_sbom'] else "N/A",
        
        # JRE Distroless
        "amd64_distroless_size": variants['dist']['amd64']['size'],
        "arm64_distroless_size": variants['dist']['arm64']['size'],
        "amd64_dist_full_sha": build_full_sha(variants['dist']['ghcr_tag'], variants['dist']['amd64']['digest']),
        "arm64_dist_full_sha": build_full_sha(variants['dist']['ghcr_tag'], variants['dist']['arm64']['digest']),
        "amd64_distroless_digest": f"`{metadata[targets['dist']].get('containerimage.digest', 'N/A')}`",
        "dist_sbom_url": variants['dist']['artifacts']['sbom'] if variants['dist']['artifacts']['sbom'] else "N/A",
        "dist_provenance_url": variants['dist']['artifacts']['provenance'] if variants['dist']['artifacts']['provenance'] else "N/A",
        "dist_attestation_url": variants['dist']['artifacts']['attestation'] if variants['dist']['artifacts']['attestation'] else "N/A",
        "dist_cosign_sbom": variants['dist']['artifacts']['cosign_sbom'] if variants['dist']['artifacts']['cosign_sbom'] else "N/A",
        
        # Legacy naming (backward compatibility)
        "amd64_jdk_sbom": f"https://{variants['jdk']['ghcr_tag']}" if variants['jdk']['ghcr_tag'] else "N/A",
        "amd64_jre_sbom": f"https://{variants['jre']['ghcr_tag']}" if variants['jre']['ghcr_tag'] else "N/A",
        "amd64_distroless_sbom": f"https://{variants['dist']['ghcr_tag']}" if variants['dist']['ghcr_tag'] else "N/A",
    }

    # قراءة وتنفيذ الـ template
    try:
        with open(args_cli.template, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        tpl = Template(template_content)
        rendered = tpl.render(context)
        
        # كتابة الناتج
        output_dir = os.path.dirname(args_cli.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(args_cli.output, 'w', encoding='utf-8') as f:
            f.write(rendered)
        
        print(f"\n✅ README generated successfully: {args_cli.output}")
        
    except FileNotFoundError:
        print(f"❌ Error: Template file not found: {args_cli.template}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: Failed to generate README: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()