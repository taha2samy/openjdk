# syntax=docker/dockerfile:1
ARG WOLFI_BASE_DIGEST
ARG WOLFI_STATIC_DIGEST

FROM alpine:3.19 AS fetcher
ARG TARGETARCH
ARG JAVA_URL_AMD64
ARG JAVA_URL_AARCH64
ARG JAVA_SHA_AMD64
ARG JAVA_SHA_AARCH64
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache curl tar
RUN set -ux; \
    if [ "$TARGETARCH" = "amd64" ]; then \
    URL=$JAVA_URL_AMD64; SHA=$JAVA_SHA_AMD64; \
    else \
    URL=$JAVA_URL_AARCH64; SHA=$JAVA_SHA_AARCH64; \
    fi; \
    curl -LfsS "$URL" -o java.tar.gz && \
    echo "$SHA  java.tar.gz" | sha256sum -c - && \
    mkdir -p /opt/java-full && \
    tar -xzf java.tar.gz -C /opt/java-full --strip-components=1 && \
    rm java.tar.gz

FROM cgr.dev/chainguard/wolfi-base@${WOLFI_BASE_DIGEST} AS cleaner
COPY --from=fetcher /opt/java-full /opt/java-slim
RUN rm -rf /opt/java-slim/jmods \
    /opt/java-slim/lib/src.zip \
    /opt/java-slim/demo \
    /opt/java-slim/sample \
    /opt/java-slim/man \
    /opt/java-slim/docs

FROM cgr.dev/chainguard/wolfi-base@${WOLFI_BASE_DIGEST} AS helper
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache libstdc++ zlib tzdata
RUN addgroup -g 1000 java && adduser -u 1000 -G java -D -s /bin/bash java
RUN mkdir -p /etc && touch /etc/nsswitch.conf && ln -sf /usr/lib/libz.so.1 /usr/lib/libz.so

FROM cgr.dev/chainguard/wolfi-base@${WOLFI_BASE_DIGEST} AS jdk-standard
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache libstdc++ zlib tzdata bash curl
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=fetcher /opt/java-full /opt/java
ENV JAVA_HOME=/opt/java
ENV PATH="/opt/java/bin:${PATH}"
USER java
WORKDIR /home/java
ENTRYPOINT ["/opt/java/bin/java", "-jar"]

FROM cgr.dev/chainguard/wolfi-base@${WOLFI_BASE_DIGEST} AS jre-standard
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache libstdc++ zlib tzdata bash curl
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=cleaner /opt/java-slim /opt/java
ENV JAVA_HOME=/opt/java
ENV PATH="/opt/java/bin:${PATH}"
USER java
WORKDIR /home/java
ENTRYPOINT ["/opt/java/bin/java", "-jar"]

FROM cgr.dev/chainguard/static@${WOLFI_STATIC_DIGEST} AS jre-distroless
COPY --from=helper /etc/passwd /etc/group /etc/
COPY --from=helper /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=helper /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=helper /usr/lib/libstdc++.so.6* /usr/lib/
COPY --from=helper /usr/lib/libgcc_s.so.1 /usr/lib/
COPY --from=helper /usr/lib/libz.so* /usr/lib/
COPY --from=helper /lib/ld-linux-x86-64.so.2* /lib/ 2>/dev/null || true
COPY --from=helper /lib/ld-linux-aarch64.so.1* /lib/ 2>/dev/null || true
COPY --from=cleaner /opt/java-slim /opt/java
ENV JAVA_HOME=/opt/java
ENV PATH="/opt/java/bin:${PATH}"
ENV LANG=C.UTF-8
USER java
WORKDIR /home/java
ENTRYPOINT ["/opt/java/bin/java", "-jar"]