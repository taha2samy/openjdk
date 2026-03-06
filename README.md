

# Wolfi Java FIPS (High-Assurance Runtime)

[![FIPS 140-3](https://img.shields.io/badge/FIPS-140--3%20Enforced-blue?style=for-the-badge&logo=shield)](https://taha2samy.github.io/openjdk/)
[![Zero CVE](https://img.shields.io/badge/Zero--CVE-Wolfi%20OS-brightgreen?style=for-the-badge)](https://taha2samy.github.io/openjdk/)
[![SLSA Level 3](https://img.shields.io/badge/SLSA-Level%203-orange?style=for-the-badge)](https://taha2samy.github.io/openjdk/)

A suite of hardened, **FIPS 140-3 compliant** Java Container Images designed for mission-critical workloads. Built on the **Wolfi OS** (undistro) ecosystem and powered by **Eclipse Temurin (Adoptium)** binaries with **Bouncy Castle FIPS** integration.

## 🛡️ Architecture & Hardening

This project implements a **Hardened Cryptographic Boundary** by overriding the default JVM security stack:

1.  **Wolfi Base:** Glibc-based zero-CVE foundation with minimal attack surface.
2.  **Strict FIPS Enforcement:** Bouncy Castle FIPS (BC-FJA) is injected as the primary security provider.
3.  **Runtime Guardrails:** System properties are locked at the JVM level (`approved_only=true`) to explicitly reject non-approved algorithms (MD5, DES, RSA < 2048).
4.  **KeyStore Integrity:** Automatic conversion of system `cacerts` to **BCFKS** (Bouncy Castle FIPS KeyStore) format.
5.  **Supply Chain Security:** SLSA Level 3 compliant pipeline with signed artifacts and full provenance.

## 🚀 Image Flavors

We provide three tiers for every LTS version (8, 11, 17, 21, 25):

| Flavor | Description | Target Use-case |
| :--- | :--- | :--- |
| `jdk_standard` | Full SDK + Shell + Package Manager | CI/CD Build Stage |
| `jre_standard` | Optimized Runtime + Basic Shell | Production (Standard) |
| `jre_distroless` | **No Shell / No APK / Non-Root** | High-Security Production |

## 🧪 Continuous Validation

Every image version undergoes a rigorous automated test suite (32+ Assertions) covering:
- **Positive Tests:** TLS 1.3 connectivity, BCFKS loading, SHA-256/AES-GCM verification.
- **Negative Tests:** Verification that the boundary successfully **blocks** MD5, MD4, Triple-DES, and weak RSA keys.

Detailed compliance reports are available on our [Security Dashboard](https://taha2samy.github.io/openjdk/).

## 📦 Usage

```bash
# Example: Pulling Java 21 Hardened Runtime
docker pull ghcr.io/taha2samy/java:21-jre_distroless
```

The `ENTRYPOINT` is pre-configured to `/opt/java/bin/java`. All security properties are injected via `JAVA_TOOL_OPTIONS`, requiring zero changes to your application code for FIPS enforcement.

---

## 🔗 Project Links
- **Documentation & Reports:** [https://taha2samy.github.io/openjdk/](https://taha2samy.github.io/openjdk/)
- **Registry:** [GitHub Container Registry](https://github.com/taha2samy/openjdk/pkgs/container/java)

