import json
import sys
import os
import datetime
import subprocess
import logging
from typing import Dict, Any


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

log = logging.getLogger(__name__)


class DependencyUploader:
    def __init__(self, file_path: str, target: str, repo: str):
        self.file_path = file_path
        self.target = target
        self.repo = repo
        self.sha = os.environ.get("GITHUB_SHA")
        self.ref = os.environ.get("GITHUB_REF")
        self.run_id = os.environ.get("GITHUB_RUN_ID", "manual")
        self.scanned_time = datetime.datetime.utcnow().isoformat() + "Z"

    def _build_payload(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            log.error(f"File not found: {self.file_path}")
            sys.exit(1)

        with open(self.file_path, "r") as f:
            sbom_data = json.load(f)

        components = sbom_data.get("components", [])
        log.info(f"Processing {len(components)} components from {self.file_path}")

        resolved = {}
        for comp in components:
            purl = comp.get("purl")
            if purl:
                resolved[purl] = {
                    "package_url": purl,
                    "relationship": "direct",
                    "scope": "runtime"
                }

        manifest_id = f"wolfi-{self.target}"
        manifests = {
            manifest_id: {
                "name": manifest_id,
                "file": {"source_location": self.file_path},
                "resolved": resolved
            }
        }

        return {
            "version": 0,
            "sha": self.sha,
            "ref": self.ref,
            "job": {
                "correlator": f"wolfi-fips-{self.target}",
                "id": self.run_id
            },
            "detector": {
                "name": "wolfi-fips-uploader",
                "version": "1.3.0",
                "url": "https://github.com/taha2samy"
            },
            "scanned": self.scanned_time,
            "manifests": manifests
        }

    def run(self):
        try:
            payload = self._build_payload()
            log.info(f"Uploading snapshot to {self.repo}")

            result = subprocess.run(
                [
                    "gh", "api",
                    f"/repos/{self.repo}/dependency-graph/snapshots",
                    "--method", "POST",
                    "--input", "-"
                ],
                input=json.dumps(payload),
                text=True,
                capture_output=True
            )

            if result.returncode != 0:
                log.error(f"GitHub API Error: {result.stderr.strip()}")
                sys.exit(1)

            log.info(f"Successfully updated dependency graph for {self.target}")

        except Exception as e:
            log.exception(f"Unexpected failure: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        log.error("Usage: python3 upload_sbom.py <FILE_PATH> <TARGET> <REPO>")
        sys.exit(1)

    uploader = DependencyUploader(
        file_path=sys.argv[1],
        target=sys.argv[2],
        repo=sys.argv[3]
    )
    uploader.run()