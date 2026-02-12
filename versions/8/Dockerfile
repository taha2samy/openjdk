# syntax=docker/dockerfile:1

ARG BC_FIPS_URL="https://repo1.maven.org/maven2/org/bouncycastle/bc-fips/2.1.2/bc-fips-2.1.2.jar"
ARG BCUTIL_FIPS_URL="https://repo1.maven.org/maven2/org/bouncycastle/bcutil-fips/2.1.5/bcutil-fips-2.1.5.jar"
ARG BCTLS_FIPS_URL="https://repo1.maven.org/maven2/org/bouncycastle/bctls-fips/2.1.22/bctls-fips-2.1.22.jar"

FROM alpine:3.19 AS fetcher
ARG TARGETARCH
ARG JAVA_URL_AMD64
ARG JAVA_URL_AARCH64
ARG JAVA_SHA_AMD64
ARG JAVA_SHA_AARCH64

RUN --mount=type=cache,target=/var/cache/java_download,id=java_downloads_{{ version }} \
    apk add --no-cache curl tar && \
    if [ "$TARGETARCH" = "amd64" ]; then URL=$JAVA_URL_AMD64; SHA=$JAVA_SHA_AMD64; \
    else URL=$JAVA_URL_AARCH64; SHA=$JAVA_SHA_AARCH64; fi; \
    FILENAME=$(basename "$URL"); \
    if [ ! -f "/var/cache/java_download/$FILENAME" ]; then curl -LfsS "$URL" -o "/var/cache/java_download/$FILENAME"; fi; \
    echo "$SHA  /var/cache/java_download/$FILENAME" | sha256sum -c - && \
    mkdir -p /opt/java-full && tar -xzf "/var/cache/java_download/$FILENAME" -C /opt/java-full --strip-components=1

FROM cgr.dev/chainguard/wolfi-base AS cleaner
COPY --from=fetcher /opt/java-full /opt/java-slim
{% if version == '8' %}
RUN rm -rf /opt/java-slim/src.zip /opt/java-slim/demo /opt/java-slim/sample /opt/java-slim/man
{% else %}
RUN rm -rf /opt/java-slim/jmods /opt/java-slim/lib/src.zip /opt/java-slim/demo /opt/java-slim/sample /opt/java-slim/man /opt/java-slim/docs
{% endif %}

FROM cleaner AS fips-modifier
USER root
ARG BC_FIPS_URL
ARG BCUTIL_FIPS_URL
ARG BCTLS_FIPS_URL
RUN apk add --no-cache curl ca-certificates

COPY migrate.js /tmp/migrate.js
COPY java.security /tmp/java.security

RUN curl -fLso /tmp/bc-fips.jar "$BC_FIPS_URL" && \
    curl -fLso /tmp/bcutil-fips.jar "$BCUTIL_FIPS_URL" && \
    curl -fLso /tmp/bctls-fips.jar "$BCTLS_FIPS_URL" && \
    curl -fLso /tmp/cacert.pem https://curl.se/ca/cacert.pem

RUN CACERTS_PATH=$(find /opt/ -name cacerts | head -n 1) && \
    J_SEC_DIR=$(dirname "$CACERTS_PATH") && \
    if [ "{{ version }}" = "8" ]; then J_EXT_DIR=$(find /opt/java-slim -name ext -type d | head -n 1); else J_EXT_DIR="/opt/java-slim/lib"; fi && \
    env JAVA_TOOL_OPTIONS="" /opt/java-slim/bin/jjs -scripting -cp /tmp/bc-fips.jar /tmp/migrate.js && \
    mv /tmp/cacerts.bcfks "$CACERTS_PATH" && \
    cp /tmp/bc-fips.jar /tmp/bcutil-fips.jar /tmp/bctls-fips.jar "$J_EXT_DIR/" && \
    cp /tmp/java.security "$J_SEC_DIR/java.security"

FROM cgr.dev/chainguard/wolfi-base AS helper
RUN apk add --no-cache libstdc++ zlib tzdata posix-libc-utils ca-certificates
RUN (addgroup -g 1001 java || true) && (adduser -u 1001 -G java -D -s /bin/bash java || true)
RUN mkdir -p /etc && touch /etc/nsswitch.conf && ln -sf /usr/lib/libz.so.1 /usr/lib/libz.so
RUN cp /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

FROM cgr.dev/chainguard/wolfi-base AS jdk-standard
RUN apk add --no-cache libstdc++ zlib tzdata bash curl posix-libc-utils ca-certificates
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=helper /etc/localtime /etc/localtime
COPY --from=helper /etc/timezone /etc/timezone
COPY --from=fips-modifier /opt/java-slim /opt/java
RUN chown -R java:java /opt/java
ENV JAVA_HOME=/opt/java PATH="/opt/java/bin:${PATH}"
ENV JAVA_TOOL_OPTIONS="-Dorg.bouncycastle.fips.approved_only=true -Dorg.bouncycastle.rsa.allow_sha1_sig=true -Dorg.bouncycastle.jsse.client.assumeExtendedKeyUsage=false -Djdk.tls.trustNameService=true -Dkeystore.type=BCFKS -Djavax.net.ssl.trustStore=/opt/java/jre/lib/security/cacerts -Djavax.net.ssl.trustStoreType=BCFKS -Djavax.net.ssl.trustStorePassword=changeit"
ENTRYPOINT []
USER java
WORKDIR /home/java

FROM cgr.dev/chainguard/wolfi-base AS jre-standard
RUN apk add --no-cache libstdc++ zlib tzdata bash curl posix-libc-utils bash ca-certificates
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=fips-modifier /opt/java-slim /opt/java
RUN chown -R java:java /opt/java
ENV JAVA_HOME=/opt/java PATH="/opt/java/bin:${PATH}"
ENV JAVA_TOOL_OPTIONS="-Dorg.bouncycastle.fips.approved_only=true -Dorg.bouncycastle.rsa.allow_sha1_sig=true -Dorg.bouncycastle.jsse.client.assumeExtendedKeyUsage=false -Djdk.tls.trustNameService=true -Dkeystore.type=BCFKS -Djavax.net.ssl.trustStore=/opt/java/jre/lib/security/cacerts -Djavax.net.ssl.trustStoreType=BCFKS -Djavax.net.ssl.trustStorePassword=changeit"
ENTRYPOINT []
USER java
WORKDIR /home/java

FROM cgr.dev/chainguard/static AS jre-distroless
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=helper /etc/localtime /etc/localtime
COPY --from=helper /etc/timezone /etc/timezone
COPY --from=helper /etc/ssl/certs /etc/ssl/certs
COPY --from=helper /usr/lib/libstdc++.so* /usr/lib/
COPY --from=helper /usr/lib/libgcc_s.so* /usr/lib/
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=helper /usr/lib/libc.so* /usr/lib/
COPY --from=helper /usr/lib/libpthread.so* /usr/lib/
COPY --from=helper /usr/lib/libm.so* /usr/lib/
COPY --from=helper /usr/lib/libdl.so* /usr/lib/
COPY --from=helper /usr/lib/librt.so* /usr/lib/
COPY --from=helper /lib/ld-linux-* /lib/
COPY --from=fips-modifier /opt/java-slim /opt/java
ENV JAVA_HOME=/opt/java PATH="/opt/java/bin:${PATH}" LANG=C.UTF-8 TZ=UTC
ENV JAVA_TOOL_OPTIONS="-Dorg.bouncycastle.fips.approved_only=true -Dorg.bouncycastle.rsa.allow_sha1_sig=true -Dorg.bouncycastle.jsse.client.assumeExtendedKeyUsage=false -Djdk.tls.trustNameService=true -Dkeystore.type=BCFKS -Djavax.net.ssl.trustStore=/opt/java/jre/lib/security/cacerts -Djavax.net.ssl.trustStoreType=BCFKS -Djavax.net.ssl.trustStorePassword=changeit"
USER java
WORKDIR /home/java
ENTRYPOINT ["/opt/java/bin/java"]