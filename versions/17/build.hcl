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

variable "CACHE_TAG" {
    default = "cache-17"
}
variable "REGISTRY" {}
variable "WOLFI_BASE_DIGEST" {}
variable "WOLFI_STATIC_DIGEST" {}

target "_java17-common" {
    inherits = ["_common"]
    args = {
        JAVA_VER             = "17"
        JAVA_FULL_VERSION    = JAVA17_FULL_VER
        JAVA_SECURITY_LEVEL  = JAVA17_SEC_LEVEL
        JAVA_SEMVER          = JAVA17_SEMVER
        JAVA_SCM_REF         = JAVA17_SCM_REF
        JAVA_UPSTREAM_UPDATE = JAVA17_UPSTREAM_UPDATE
        WOLFI_BASE_DIGEST    = WOLFI_BASE_DIGEST
        WOLFI_STATIC_DIGEST  = WOLFI_STATIC_DIGEST
    }
}

target "java17-jre-std" {
    inherits = ["_java17-common"] 
    context  = "./versions/17"
    target   = "jre-standard"
    args     = {
        BUILD_TYPE       = "jre"
        JAVA_URL_AMD64   = JAVA17_JRE_AMD64_URL
        JAVA_SHA_AMD64   = JAVA17_JRE_AMD64_SHA
        JAVA_URL_AARCH64 = JAVA17_JRE_ARM64_URL
        JAVA_SHA_AARCH64 = JAVA17_JRE_ARM64_SHA
    }
    tags = ["${REGISTRY}/java:17-jre-std"]
}

target "java17-jdk-std" {
    inherits = ["_java17-common"]  
    context  = "./versions/17"
    target   = "jdk-standard"
    args     = {
        BUILD_TYPE       = "jdk"
        JAVA_URL_AMD64   = JAVA17_JDK_AMD64_URL
        JAVA_SHA_AMD64   = JAVA17_JDK_AMD64_SHA
        JAVA_URL_AARCH64 = JAVA17_JDK_ARM64_URL
        JAVA_SHA_AARCH64 = JAVA17_JDK_ARM64_SHA
    }
    tags = ["${REGISTRY}/java:17-jdk-std"]
}

target "java17-jre-distroless" {
    inherits = ["_java17-common"] 
    context  = "./versions/17"
    target   = "jre-distroless"
    args     = {
        BUILD_TYPE       = "jre"
        JAVA_URL_AMD64   = JAVA17_JRE_AMD64_URL
        JAVA_SHA_AMD64   = JAVA17_JRE_AMD64_SHA
        JAVA_URL_AARCH64 = JAVA17_JRE_ARM64_URL
        JAVA_SHA_AARCH64 = JAVA17_JRE_ARM64_SHA
    }
    tags = ["${REGISTRY}/java:17-jre-distroless"]
}