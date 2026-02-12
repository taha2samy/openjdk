variable "CACHE_TAG" {
default = "cache-25"
}

variable "JAVA25_JRE_AMD64_URL" {}
variable "JAVA25_JRE_AMD64_SHA" {}
variable "JAVA25_JRE_ARM64_URL" {}
variable "JAVA25_JRE_ARM64_SHA" {}
variable "JAVA25_JDK_AMD64_URL" {}
variable "JAVA25_JDK_AMD64_SHA" {}
variable "JAVA25_JDK_ARM64_URL" {}
variable "JAVA25_JDK_ARM64_SHA" {}
variable "JAVA25_FULL_VER" {}
variable "JAVA25_SEC_LEVEL" {}
variable "JAVA25_SEMVER" {}
variable "JAVA25_SCM_REF" {}
variable "JAVA25_UPSTREAM_UPDATE" {}

target "_java25-common" {
inherits = ["_common"]
args = {
JAVA_VER = "25"
JAVA_FULL_VERSION = JAVA25_FULL_VER
JAVA_SECURITY_LEVEL = JAVA25_SEC_LEVEL
JAVA_SEMVER = JAVA25_SEMVER
JAVA_SCM_REF = JAVA25_SCM_REF
JAVA_UPSTREAM_UPDATE = JAVA25_UPSTREAM_UPDATE
WOLFI_BASE_DIGEST = WOLFI_BASE_DIGEST
WOLFI_STATIC_DIGEST = WOLFI_STATIC_DIGEST
}
}

target "java25-jre-std" {
inherits = ["_java25-common"]
context = "./versions/25"
target = "jre-standard"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA25_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA25_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA25_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA25_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:25-jre-std", "${GHCR_REGISTRY}/${REPO_GHCR}:25-jre-std"]
}

target "java25-jdk-std" {
inherits = ["_java25-common"]
context = "./versions/25"
target = "jdk-standard"
args = {
BUILD_TYPE = "jdk"
JAVA_URL_AMD64 = JAVA25_JDK_AMD64_URL
JAVA_SHA_AMD64 = JAVA25_JDK_AMD64_SHA
JAVA_URL_AARCH64 = JAVA25_JDK_ARM64_URL
JAVA_SHA_AARCH64 = JAVA25_JDK_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:25-jdk-std", "${GHCR_REGISTRY}/${REPO_GHCR}:25-jdk-std"]
}

target "java25-jre-distroless" {
inherits = ["_java25-common"]
context = "./versions/25"
target = "jre-distroless"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA25_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA25_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA25_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA25_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:25-jre-distroless", "${GHCR_REGISTRY}/${REPO_GHCR}:25-jre-distroless"]
}