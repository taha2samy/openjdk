---
hide:
  - navigation
  - toc
---

<div class="java-hero" markdown>
# :fontawesome-brands-java: Wolfi Java FIPS
**High-Assurance Cryptographic Foundation for Cloud-Native Workloads**
</div>

<div style="text-align: center; margin-top: -20px; margin-bottom: 40px; font-size: 1.2rem; color: var(--md-default-fg-color--light);">
A secure, zero-CVE, and fully FIPS 140-3 compliant Java environment built for modern Kubernetes and Docker infrastructure.
</div>

---

## :material-pillar: Core Architecture

<div class="grid cards" markdown>

-   :material-shield-check: **Zero-CVE Base (Wolfi OS)**
    ---
    Built on top of the **Wolfi** undistro. Designed for the container era to provide a minimalist attack surface with rolling updates, ensuring continuous Zero-CVE compliance.

-   :material-lock-check: **Strict FIPS 140-3 Enforcement**
    ---
    Integrated with **Bouncy Castle FIPS (BC-FJA)**. Hardcoded at the JVM level (`approved_only=true`) to strictly reject any non-approved cryptographic algorithms (e.g., MD5).

-   :material-coffee: **Enterprise Java (Adoptium)**
    ---
    Powered by **Eclipse Temurin** upstream binaries. Delivering rock-solid performance, stability, and seamless compatibility for Java 8, 11, 17, 21, and 25 LTS.

</div>

---

## :material-layers-triple: Artifact Tiers

We provide three distinct image flavors for every supported Java version, ensuring you have the exact toolset required for your stage in the SDLC:

<div class="grid cards" markdown>

-   :material-shield-off-outline: **Production Distroless**
    ---
    `jre_distroless`
    <br>
    The ultimate production target. Contains only the JRE and strictly required libraries. **Zero shell, zero package manager, zero system utilities.**

-   :material-package-variant: **Standard Image**
    ---
    `jre_standard`
    <br>
    The operational production target. Contains the JRE along with a basic shell (`ash`) and minimal utilities required for debugging and orchestration hooks.

-   :material-toolbox-outline: **Development SDK**
    ---
    `jdk_standard`
    <br>
    The builder environment. Contains the full JDK (compilers, tools), shell, and package manager (`apk`). Designed strictly for CI/CD pipelines.

</div>

---

## :material-file-document-check-outline: Continuous Validation

Every image in this repository undergoes rigorous static analysis and compliance validation before publishing. 

*   :material-shield-bug: **Vulnerability Scanning:** Deep inspection of all layers using Trivy.
*   :fontawesome-brands-docker: **Docker CIS:** Automated validation against CIS Docker Benchmarks.
*   :material-kubernetes: **NSA K8s Hardening:** Verified against NSA/CISA Container build guidelines.
*   :material-security: **K8s PSS Restricted:** Architected to pass Kubernetes Pod Security Standards.

---

## :material-bookshelf: Supported LTS Versions

Select your target Java LTS version to explore available tags, immutable digests, and detailed static analysis reports.

<div class="grid cards" markdown>

-   [:fontawesome-brands-java: **Java 8 LTS**](java-8.md)
    ---
    *Legacy enterprise support with strict FIPS enforcement.*

-   [:fontawesome-brands-java: **Java 11 LTS**](java-11.md)
    ---
    *Stable transition layer for modern applications.*

-   [:fontawesome-brands-java: **Java 17 LTS**](java-17.md)
    ---
    *Current enterprise standard with optimized performance.*

-   [:fontawesome-brands-java: **Java 21 LTS**](java-21.md)
    ---
    *Next-gen runtime featuring Project Loom (Virtual Threads).*

-   [:fontawesome-brands-java: **Java 25 LTS**](java-25.md)
    ---
    *Latest long-term support release for future-proofing.*

</div>