variable "CACHE_TAG" {
default = "cache-8"
}

variable "JAVA8_JRE_AMD64_URL" {}
variable "JAVA8_JRE_AMD64_SHA" {}
variable "JAVA8_JRE_ARM64_URL" {}
variable "JAVA8_JRE_ARM64_SHA" {}
variable "JAVA8_JDK_AMD64_URL" {}
variable "JAVA8_JDK_AMD64_SHA" {}
variable "JAVA8_JDK_ARM64_URL" {}
variable "JAVA8_JDK_ARM64_SHA" {}
variable "JAVA8_FULL_VER" {}
variable "JAVA8_SEC_LEVEL" {}
variable "JAVA8_SEMVER" {}
variable "JAVA8_SCM_REF" {}
variable "JAVA8_UPSTREAM_UPDATE" {}

target "_java8-common" {
inherits = ["_common"]
args = {
JAVA_VER = "8"
JAVA_FULL_VERSION = JAVA8_FULL_VER
JAVA_SECURITY_LEVEL = JAVA8_SEC_LEVEL
JAVA_SEMVER = JAVA8_SEMVER
JAVA_SCM_REF = JAVA8_SCM_REF
JAVA_UPSTREAM_UPDATE = JAVA8_UPSTREAM_UPDATE
WOLFI_BASE_DIGEST = WOLFI_BASE_DIGEST
WOLFI_STATIC_DIGEST = WOLFI_STATIC_DIGEST
}
}

target "java8-jre-std" {
inherits = ["_java8-common"]
context = "./versions/8"
target = "jre-standard"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA8_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA8_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA8_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA8_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:8-jre-std", "${GHCR_REGISTRY}/${REPO_GHCR}:8-jre-std"]
}

target "java8-jdk-std" {
inherits = ["_java8-common"]
context = "./versions/8"
target = "jdk-standard"
args = {
BUILD_TYPE = "jdk"
JAVA_URL_AMD64 = JAVA8_JDK_AMD64_URL
JAVA_SHA_AMD64 = JAVA8_JDK_AMD64_SHA
JAVA_URL_AARCH64 = JAVA8_JDK_ARM64_URL
JAVA_SHA_AARCH64 = JAVA8_JDK_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:8-jdk-std", "${GHCR_REGISTRY}/${REPO_GHCR}:8-jdk-std"]
}

target "java8-jre-distroless" {
inherits = ["_java8-common"]
context = "./versions/8"
target = "jre-distroless"
args = {
BUILD_TYPE = "jre"
JAVA_URL_AMD64 = JAVA8_JRE_AMD64_URL
JAVA_SHA_AMD64 = JAVA8_JRE_AMD64_SHA
JAVA_URL_AARCH64 = JAVA8_JRE_ARM64_URL
JAVA_SHA_AARCH64 = JAVA8_JRE_ARM64_SHA
}
tags = ["${DOCKER_REGISTRY}/${REPO_DOCKER}:8-jre-distroless", "${GHCR_REGISTRY}/${REPO_GHCR}:8-jre-distroless"]
}