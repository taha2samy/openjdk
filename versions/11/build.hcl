variable "CACHE_TAG" {
default = "cache-11"
}

variable "JAVA11_JRE_AMD64_URL" {}
variable "JAVA11_JRE_AMD64_SHA" {}
variable "JAVA11_JRE_ARM64_URL" {}
variable "JAVA11_JRE_ARM64_SHA" {}
variable "JAVA11_JDK_AMD64_URL" {}
variable "JAVA11_JDK_AMD64_SHA" {}
variable "JAVA11_JDK_ARM64_URL" {}
variable "JAVA11_JDK_ARM64_SHA" {}
variable "JAVA11_FULL_VER" {}
variable "JAVA11_SEC_LEVEL" {}
variable "JAVA11_SEMVER" {}
variable "JAVA11_SCM_REF" {}
variable "JAVA11_UPSTREAM_UPDATE" {}

target "_java11-common" {
inherits = ["_common"]
args = {
JAVA_VER = "11"
JAVA_FULL_VERSION = JAVA11_FULL_VER
JAVA_SECURITY_LEVEL = JAVA11_SEC_LEVEL
JAVA_SEMVER = JAVA11_SEMVER
JAVA_SCM_REF = JAVA11_SCM_REF
JAVA_UPSTREAM_UPDATE = JAVA11_UPSTREAM_UPDATE
WOLFI_BASE_DIGEST = WOLFI_BASE_DIGEST
WOLFI_STATIC_DIGEST = WOLFI_STATIC_DIGEST
}
}

target "java11-jre-std" {
inherits = ["_java11-common"]
context = "./versions/11"
target = "jre-standard"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA11_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA11_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA11_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA11_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:11-jre-std", "${GHCR_REGISTRY}/${REPO_GHCR}:11-jre-std"]
}

target "java11-jdk-std" {
inherits = ["_java11-common"]
context = "./versions/11"
target = "jdk-standard"
args = {
BUILD_TYPE = "jdk"
JAVA_URL_AMD64 = JAVA11_JDK_AMD64_URL
JAVA_SHA_AMD64 = JAVA11_JDK_AMD64_SHA
JAVA_URL_AARCH64 = JAVA11_JDK_ARM64_URL
JAVA_SHA_AARCH64 = JAVA11_JDK_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:11-jdk-std", "${GHCR_REGISTRY}/${REPO_GHCR}:11-jdk-std"]
}

target "java11-jre-distroless" {
inherits = ["_java11-common"]
context = "./versions/11"
target = "jre-distroless"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA11_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA11_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA11_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA11_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:11-jre-distroless", "${GHCR_REGISTRY}/${REPO_GHCR}:11-jre-distroless"]
}