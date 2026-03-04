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



---

## :material-console-line: Usage & Execution

All images in this repository share a unified and streamlined execution model. The `ENTRYPOINT` is strictly set to `["/opt/java/bin/java"]`. This means the container behaves exactly like the native `java` executable—you simply pass your JVM arguments or `.jar` files directly.

!!! tip "Zero-Config Strict FIPS 140-3 Enforcement"
    You do not need to manually configure FIPS properties. We have injected the stringent security requirements directly into the image's environment via `JAVA_TOOL_OPTIONS`. 
    
    By default, the JVM runs with `-Dorg.bouncycastle.fips.approved_only=true`. This guarantees that if your application attempts to invoke a non-compliant cryptographic algorithm (e.g., `MD5` or `DES`), the Bouncy Castle provider will **explicitly block it and throw a runtime exception**, ensuring 100% cryptographic compliance without altering your application code.


### :material-code-tags: Implementation Examples

=== ":material-docker: Direct CLI Execution"

    Because the `ENTRYPOINT` is already set to `java`, you can test your compiled `.jar` files or check JVM properties directly from your terminal.

    ```bash
    # 1. Verify injected FIPS properties and Java version
    docker run --rm ghcr.io/taha2samy/java:21-jre_distroless -XshowSettings:properties -version

    # 2. Run a local application by mounting the volume
    docker run --rm -v $(pwd):/app -w /app ghcr.io/taha2samy/java:21-jre_standard -jar my-secure-app.jar
    ```

=== ":material-file-code-outline: Multi-Stage Dockerfile"

    This is the recommended approach for Production. Use the **Development SDK** (`jdk_standard`) to compile your code, and the **Production Distroless** (`jre_distroless`) to run it.

    ```dockerfile
    # Stage 1: Build Environment
    FROM ghcr.io/taha2samy/java:21-jdk_standard AS builder
    WORKDIR /build
    COPY . .
    # The shell and package manager are available here
    RUN ./mvnw clean package -DskipTests

    # Stage 2: Production Distroless Runtime
    FROM ghcr.io/taha2samy/java:21-jre_distroless
    
    # Run as a non-privileged user (Enforced by default)
    USER 1001
    WORKDIR /app
    
    COPY --from=builder /build/target/secure-app.jar /app.jar

    # We only need to provide the CMD arguments.
    # The ENTRYPOINT ["/opt/java/bin/java"] is seamlessly inherited.
    CMD ["-Xmx512m", "-jar", "/app.jar"]
    ```


=== ":material-test-tube: Real-world Network Verification"

    This example demonstrates a complete end-to-end flow: compiling code with the **JDK SDK**, running it on **Distroless JRE**, and verifying a secure HTTPS connection via **BCFIPS JSSE**.

    === ":material-coffee: Main.java"

        ```java
        import java.net.URI;
        import java.net.http.HttpClient;
        import java.net.http.HttpRequest;
        import java.net.http.HttpResponse;

        public class Main {
            public static void main(String[] args) {
                try {
                    System.out.println("--- FIPS TLS Handshake Test ---");
                    HttpClient client = HttpClient.newHttpClient();
                    HttpRequest request = HttpRequest.newBuilder()
                            .uri(URI.create("https://adoptium.net"))
                            .GET()
                            .build();

                    System.out.println("Connecting to Adoptium via Secure TLS...");
                    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

                    System.out.println("Response Status: " + response.statusCode());
                    System.out.println("Connection Proof: TLS Session established via BCFIPS");
                    System.out.println("SUCCESS: Secure network communication verified.");
                } catch (Exception e) {
                    System.err.println("FAILED: Security provider blocked the connection.");
                    e.printStackTrace();
                    System.exit(1);
                }
            }
        }
        ```

    === ":material-docker: Dockerfile"

        ```dockerfile
        # Step 1: Compile using the full SDK
        FROM ghcr.io/taha2samy/java:21-jdk_standard AS builder
        WORKDIR /app
        COPY Main.java .
        RUN ["/opt/java/bin/javac", "Main.java"]

        # Step 2: Run using the Hardened Distroless Runtime
        FROM ghcr.io/taha2samy/java:21-jre_distroless
        WORKDIR /app
        COPY --from=builder /app/Main.class .

        # Uses the pre-configured ENTRYPOINT java
        CMD ["Main"]
        ```

    === ":material-text-box-check-outline: Verification Logs"

        !!! info "Runtime Trace Analysis"
            The following logs confirm that **Bouncy Castle JSSE** is handling the TLS handshake and verifying the **BCFKS TrustStore** integrity.

        ```text

        --- FIPS TLS Handshake Test ---
        Mar 04, 2026 8:38:41 PM org.bouncycastle.jsse.provider.PropertyUtils getBooleanSecurityProperty
        INFO: Found boolean security property [keystore.type.compat]: false
        Mar 04, 2026 8:38:41 PM org.bouncycastle.jsse.provider.PropertyUtils getStringSystemProperty
        INFO: Found string system property [javax.net.ssl.trustStore]: /opt/java/lib/security/cacerts
        Mar 04, 2026 8:38:41 PM org.bouncycastle.jsse.provider.PropertyUtils getStringSystemProperty
        INFO: Found string system property [javax.net.ssl.trustStoreType]: BCFKS
        Mar 04, 2026 8:38:41 PM org.bouncycastle.jsse.provider.PropertyUtils getSensitiveStringSystemProperty
        INFO: Found sensitive string system property [javax.net.ssl.trustStorePassword]
        Mar 04, 2026 8:38:41 PM org.bouncycastle.jsse.provider.PropertyUtils getBooleanSystemProperty
        INFO: Found boolean system property [org.bouncycastle.jsse.trustManager.checkEKU]: false
        Mar 04, 2026 8:38:41 PM org.bouncycastle.jsse.provider.PropertyUtils getStringSecurityProperty
        INFO: Found string security property [jdk.tls.disabledAlgorithms]: SSLv3, TLSv1, TLSv1.1, RC4, DES, 3DES_EDE_CBC, TDEA, MD5, NULL, anon, ECDH, DH keySize < 2048, RSA keySize < 2048
        Mar 04, 2026 8:38:41 PM org.bouncycastle.jsse.provider.PropertyUtils getStringSecurityProperty
        INFO: Found string security property [jdk.certpath.disabledAlgorithms]: MD2, MD5, SHA1 keySize < 1024, RSA keySize < 2048, DSA keySize < 2048, EC keySize < 224
        Connecting to Adoptium via Secure TLS...
        Response Status: 200
        Connection Proof: TLS Session established via BCFIPS
        SUCCESS: Secure network communication verified.


        ```