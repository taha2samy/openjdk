variable "JAVA17_JRE_AMD64_URL" {}
variable "JAVA17_JRE_AMD64_SHA" {}
variable "JAVA17_JRE_ARM64_URL" {}
variable "JAVA17_JRE_ARM64_SHA" {}
variable "JAVA17_JDK_AMD64_URL" {}
variable "JAVA17_JDK_AMD64_SHA" {}
variable "JAVA17_JDK_ARM64_URL" {}
variable "JAVA17_JDK_ARM64_SHA" {}
variable "JAVA17_FULL_VER" {}
variable "JAVA17_SEC_LEVEL" {}
variable "JAVA17_SEMVER" {}
variable "JAVA17_SCM_REF" {}
variable "JAVA17_UPSTREAM_UPDATE" {}

target "java17-jre-std" {
    inherits = ["_common"]
    context = "./versions/17"
    target = "jre-standard"
    args = {
        BUILD_TYPE = "jre"
        JAVA_VER = "17"
        JAVA_FULL_VERSION = JAVA17_FULL_VER
        JAVA_SECURITY_LEVEL = JAVA17_SEC_LEVEL
        JAVA_SEMVER = JAVA17_SEMVER
        JAVA_SCM_REF = JAVA17_SCM_REF
        JAVA_UPSTREAM_UPDATE = JAVA17_UPSTREAM_UPDATE
        JAVA_URL_AMD64 = JAVA17_JRE_AMD64_URL
        JAVA_SHA_AMD64 = JAVA17_JRE_AMD64_SHA
        JAVA_URL_AARCH64 = JAVA17_JRE_ARM64_URL
        JAVA_SHA_AARCH64 = JAVA17_JRE_ARM64_SHA
    }
    tags = ["${REGISTRY}/java:17-jre-wolfi"]
}

target "java17-jdk-std" {
    inherits = ["_common"]
    context = "./versions/17"
    target = "jdk-standard"
    args = {
        BUILD_TYPE = "jdk"
        JAVA_VER = "17"
        JAVA_FULL_VERSION = JAVA17_FULL_VER
        JAVA_SECURITY_LEVEL = JAVA17_SEC_LEVEL
        JAVA_SEMVER = JAVA17_SEMVER
        JAVA_SCM_REF = JAVA17_SCM_REF
        JAVA_UPSTREAM_UPDATE = JAVA17_UPSTREAM_UPDATE
        JAVA_URL_AMD64 = JAVA17_JDK_AMD64_URL
        JAVA_SHA_AMD64 = JAVA17_JDK_AMD64_SHA
        JAVA_URL_AARCH64 = JAVA17_JDK_ARM64_URL
        JAVA_SHA_AARCH64 = JAVA17_JDK_ARM64_SHA
    }
    tags = ["${REGISTRY}/java:17-jdk-wolfi"]
}

target "java17-jre-distroless" {
    inherits = ["_common"]
    context = "./versions/17"
    target = "jre-distroless"
    args = {
        BUILD_TYPE = "jre"
        JAVA_VER = "17"
        JAVA_FULL_VERSION = JAVA17_FULL_VER
        JAVA_SECURITY_LEVEL = JAVA17_SEC_LEVEL
        JAVA_SEMVER = JAVA17_SEMVER
        JAVA_SCM_REF = JAVA17_SCM_REF
        JAVA_UPSTREAM_UPDATE = JAVA17_UPSTREAM_UPDATE
        JAVA_URL_AMD64 = JAVA17_JRE_AMD64_URL
        JAVA_SHA_AMD64 = JAVA17_JRE_AMD64_SHA
        JAVA_URL_AARCH64 = JAVA17_JRE_ARM64_URL
        JAVA_SHA_AARCH64 = JAVA17_JRE_ARM64_SHA
    }
    tags = ["${REGISTRY}/java:17-jre-distroless"]
}