variable "CACHE_TAG" {
default = "cache-21"
}

variable "JAVA21_JRE_AMD64_URL" {}
variable "JAVA21_JRE_AMD64_SHA" {}
variable "JAVA21_JRE_ARM64_URL" {}
variable "JAVA21_JRE_ARM64_SHA" {}
variable "JAVA21_JDK_AMD64_URL" {}
variable "JAVA21_JDK_AMD64_SHA" {}
variable "JAVA21_JDK_ARM64_URL" {}
variable "JAVA21_JDK_ARM64_SHA" {}
variable "JAVA21_FULL_VER" {}
variable "JAVA21_SEC_LEVEL" {}
variable "JAVA21_SEMVER" {}
variable "JAVA21_SCM_REF" {}
variable "JAVA21_UPSTREAM_UPDATE" {}

target "_java21-common" {
inherits = ["_common"]
args = {
JAVA_VER = "21"
JAVA_FULL_VERSION = JAVA21_FULL_VER
JAVA_SECURITY_LEVEL = JAVA21_SEC_LEVEL
JAVA_SEMVER = JAVA21_SEMVER
JAVA_SCM_REF = JAVA21_SCM_REF
JAVA_UPSTREAM_UPDATE = JAVA21_UPSTREAM_UPDATE
WOLFI_BASE_DIGEST = WOLFI_BASE_DIGEST
WOLFI_STATIC_DIGEST = WOLFI_STATIC_DIGEST
}
}

target "java21-jre-std" {
inherits = ["_java21-common"]
context = "./versions/21"
target = "jre-standard"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA21_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA21_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA21_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA21_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:21-jre-std", "${GHCR_REGISTRY}/${REPO_GHCR}:21-jre-std"]
}

target "java21-jdk-std" {
inherits = ["_java21-common"]
context = "./versions/21"
target = "jdk-standard"
args = {
BUILD_TYPE = "jdk"
JAVA_URL_AMD64 = JAVA21_JDK_AMD64_URL
JAVA_SHA_AMD64 = JAVA21_JDK_AMD64_SHA
JAVA_URL_AARCH64 = JAVA21_JDK_ARM64_URL
JAVA_SHA_AARCH64 = JAVA21_JDK_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:21-jdk-std", "${GHCR_REGISTRY}/${REPO_GHCR}:21-jdk-std"]
}

target "java21-jre-distroless" {
inherits = ["_java21-common"]
context = "./versions/21"
target = "jre-distroless"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA21_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA21_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA21_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA21_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:21-jre-distroless", "${GHCR_REGISTRY}/${REPO_GHCR}:21-jre-distroless"]
}