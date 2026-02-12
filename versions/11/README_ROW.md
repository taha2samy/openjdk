### ☕ Java 11.0.30+7 (LTS) 

[![Docker Pulls](https://img.shields.io/docker/pulls/taha2samy/java?style=flat&logo=docker)](https://hub.docker.com/r/taha2samy/java)
![Vulnerability Scan](https://github.com/taha2samy/openjdk/actions/workflows/build-images.yml/badge.svg)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)

| 📋 Build Metadata | Information                                                  |
| :--------------- | :----------------------------------------------------------- |
| **Full Version** | `11.0.30+7`                                           |
| **Build Date**   | `2026-01-28`                                             |
| **Upstream Date**| `2026-01-28`                                          |
| **Base Image**   | `wolfi-base` (Chainguard)                                    |
| **Build Proof**  | [🔗 Provenance & Logs](https://github.com/taha2samy/openjdk/actions/runs/21684157353/attempts/1)                      |
| **Security**     | [🔍 Download SBOM (Syft)](https://github.com/taha2samy/openjdk/actions/runs/21684157353)                          |

| 📦 Image Variant    | 🏷️ Tag               | 🏗️ Architecture / 💾 Size                          | 🔐 Artifacts                                        |
| :----------------- | :------------------ | :----------------------------------------------- | :----------------------------------------------------------- |
| **JDK Standard**   | `11-jdk-std`        | 🟢 **amd64**: `202.9 MB`<br>🔵 **arm64**: `198.9 MB` | [📦 SBOM](https://github.com/taha2samy/java/attestations/0389ee5bb7156e8345fd94bf718639cae085b717c24a6eb26cb52b1b12735ffd) • [🔒 Provenance](https://github.com/taha2samy/java/attestations/0389ee5bb7156e8345fd94bf718639cae085b717c24a6eb26cb52b1b12735ffd) • [✍️ Attestation](https://github.com/taha2samy/java/attestations/0389ee5bb7156e8345fd94bf718639cae085b717c24a6eb26cb52b1b12735ffd) |
| **JRE Standard**   | `11-jre-std`        | 🟢 **amd64**: `57.7 MB`<br>🔵 **arm64**: `55.2 MB`   | [📦 SBOM](https://github.com/taha2samy/java/attestations/6304e351e5a8ed9471af9f0781e5bde1e0cdc1ba3669f2b9ea968d27055026d9) • [🔒 Provenance](https://github.com/taha2samy/java/attestations/6304e351e5a8ed9471af9f0781e5bde1e0cdc1ba3669f2b9ea968d27055026d9) • [✍️ Attestation](https://github.com/taha2samy/java/attestations/6304e351e5a8ed9471af9f0781e5bde1e0cdc1ba3669f2b9ea968d27055026d9) |
| **JRE Distroless** | `11-jre-distroless` | 🟢 **amd64**: `46.7 MB`<br>🔵 **arm64**: `44.7 MB`   | [📦 SBOM](https://github.com/taha2samy/java/attestations/cab6ad27c9cf263f12e479dc02bdc96d3492fa7348c1778c9f95289d7b1f83b9) • [🔒 Provenance](https://github.com/taha2samy/java/attestations/cab6ad27c9cf263f12e479dc02bdc96d3492fa7348c1778c9f95289d7b1f83b9) • [✍️ Attestation](https://github.com/taha2samy/java/attestations/cab6ad27c9cf263f12e479dc02bdc96d3492fa7348c1778c9f95289d7b1f83b9) |

---

#### 🏗️ Direct Image PULL (Pinned by Architecture SHA)

**JDK Standard:**
```text
Multi-arch digest: `sha256:0389ee5bb7156e8345fd94bf718639cae085b717c24a6eb26cb52b1b12735ffd`
```
- 🟢 `amd64`: `ghcr.io/taha2samy/java@sha256:7dd0fc4b19c3b26596e8a5dcb0b6715f5638a4c8ee9e915a91e355671f33ed8d`
- 🔵 `arm64`: `ghcr.io/taha2samy/java@sha256:6f1d1a72ae27c4c32d58a46f0b6e7ca4bc45bdaa322124646a41c0132b4ad09a`

**JRE Standard:**
```text
Multi-arch digest: `sha256:6304e351e5a8ed9471af9f0781e5bde1e0cdc1ba3669f2b9ea968d27055026d9`
```
- 🟢 `amd64`: `ghcr.io/taha2samy/java@sha256:4ca9689fc140bb0716946443120c6d02907db4b0196c7740c5e67895f7ffdc55`
- 🔵 `arm64`: `ghcr.io/taha2samy/java@sha256:5d12f46a0c675cf7c265ea839c892441e14197a0fc6af68fbb7e1ce887d9a6a7`

**JRE Distroless:**
```text
Multi-arch digest: `sha256:cab6ad27c9cf263f12e479dc02bdc96d3492fa7348c1778c9f95289d7b1f83b9`
```
- 🟢 `amd64`: `ghcr.io/taha2samy/java@sha256:874048d2f3e4c3a5c34eb857df5f847c8f25dfea1246de44aa9cbfc5fcb84733`
- 🔵 `arm64`: `ghcr.io/taha2samy/java@sha256:4915008ddb382be7484f82eb9b3bc800a54ccfc13570262a488af87ff3570b56`

---

#### 🔐 Security & Supply Chain

All images include:
- **SBOM** (Software Bill of Materials) - Complete dependency inventory
- **SLSA Provenance** - Build process attestation (Level 3)
- **In-toto Attestation** - Cryptographically signed metadata
- **Vulnerability Scanning** - Regular security checks via Trivy/Grype

To verify attestations:
```bash
# Verify SBOM
cosign verify-attestation --type spdx `ghcr.io/taha2samy/java@sha256:7dd0fc4b19c3b26596e8a5dcb0b6715f5638a4c8ee9e915a91e355671f33ed8d`

# Verify provenance
cosign verify-attestation --type slsaprovenance `ghcr.io/taha2samy/java@sha256:7dd0fc4b19c3b26596e8a5dcb0b6715f5638a4c8ee9e915a91e355671f33ed8d`

# Download SBOM
cosign download attestation `ghcr.io/taha2samy/java@sha256:7dd0fc4b19c3b26596e8a5dcb0b6715f5638a4c8ee9e915a91e355671f33ed8d` | jq -r '.payload' | base64 -d | jq
```

---