# syntax=docker/dockerfile:1
FROM alpine:3.19 AS fetcher
ARG TARGETARCH
ARG JAVA_URL_AMD64
ARG JAVA_URL_AARCH64
ARG JAVA_SHA_AMD64
ARG JAVA_SHA_AARCH64

RUN --mount=type=cache,target=/var/cache/java_download,id=java_downloads_11 \
    apk add --no-cache curl tar && \
    set -ux; \
    if [ "$TARGETARCH" = "amd64" ]; then \
    URL=$JAVA_URL_AMD64; SHA=$JAVA_SHA_AMD64; \
    else \
    URL=$JAVA_URL_AARCH64; SHA=$JAVA_SHA_AARCH64; \
    fi; \
    FILENAME=$(basename "$URL"); \
    if [ ! -f "/var/cache/java_download/$FILENAME" ]; then \
    curl -LfsS "$URL" -o "/var/cache/java_download/$FILENAME"; \
    fi; \
    echo "$SHA  /var/cache/java_download/$FILENAME" | sha256sum -c - && \
    mkdir -p /opt/java-full && \
    tar -xzf "/var/cache/java_download/$FILENAME" -C /opt/java-full --strip-components=1 && \
    find /opt/java-full -exec touch -t 202001010000 {} +

FROM cgr.dev/chainguard/wolfi-base@sha256:417d791afa234c538bca977fe0f44011d2381e60a9fde44c938bd17b9cc38f66 AS cleaner
COPY --from=fetcher /opt/java-full /opt/java-slim

RUN rm -rf /opt/java-slim/jmods \
    /opt/java-slim/lib/src.zip \
    /opt/java-slim/demo \
    /opt/java-slim/sample \
    /opt/java-slim/man \
    /opt/java-slim/docs


FROM cgr.dev/chainguard/wolfi-base@sha256:417d791afa234c538bca977fe0f44011d2381e60a9fde44c938bd17b9cc38f66 AS helper
RUN --mount=type=cache,target=/var/cache/apk,id=apk_cache_helper_11 \
    apk add --no-cache libstdc++ zlib tzdata posix-libc-utils
RUN addgroup -g 1000 java && adduser -u 1000 -G java -D -s /bin/bash java
RUN mkdir -p /etc && touch /etc/nsswitch.conf && ln -sf /usr/lib/libz.so.1 /usr/lib/libz.so
RUN cp /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

FROM cgr.dev/chainguard/wolfi-base@sha256:417d791afa234c538bca977fe0f44011d2381e60a9fde44c938bd17b9cc38f66 AS jdk-standard
RUN --mount=type=cache,target=/var/cache/apk,id=apk_cache_jdk_11 \
    apk add --no-cache libstdc++ zlib tzdata bash curl posix-libc-utils
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=helper /etc/localtime /etc/localtime
COPY --from=helper /etc/timezone /etc/timezone
COPY --from=fetcher /opt/java-full /opt/java
ENV JAVA_HOME=/opt/java PATH="/opt/java/bin:${PATH}"
USER java
WORKDIR /home/java


FROM cgr.dev/chainguard/wolfi-base@sha256:417d791afa234c538bca977fe0f44011d2381e60a9fde44c938bd17b9cc38f66 AS jre-standard
RUN --mount=type=cache,target=/var/cache/apk,id=apk_cache_jre_11 \
    apk add --no-cache libstdc++ zlib tzdata bash curl posix-libc-utils bash
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=cleaner /opt/java-slim /opt/java
ENV JAVA_HOME=/opt/java PATH="/opt/java/bin:${PATH}"
USER java
WORKDIR /home/java

FROM cgr.dev/chainguard/static@sha256:9cef3c6a78264cb7e25923bf1bf7f39476dccbcc993af9f4ffeb191b77a7951e AS jre-distroless
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
COPY --from=cleaner /opt/java-slim /opt/java

ENV JAVA_HOME=/opt/java \
    PATH="/opt/java/bin:${PATH}" \
    LANG=C.UTF-8 \
    TZ=UTC

USER java
WORKDIR /home/java
ENTRYPOINT ["/opt/java/bin/java"]