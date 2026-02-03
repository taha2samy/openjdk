variable "REGISTRY" {
  default = "docker.io/taha2samy"
}



variable "CACHE_TAG" {
}
target "_common" {
  platforms = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=registry,ref=${REGISTRY}/java:${CACHE_TAG}"]
  cache-to   = ["type=registry,ref=${REGISTRY}/java:${CACHE_TAG},mode=max"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]
  args = {
    WOLFI_BASE_DIGEST = WOLFI_BASE_DIGEST
    WOLFI_STATIC_DIGEST = WOLFI_STATIC_DIGEST
  }
}

group "java17" {
  targets = ["java17-jre-std", "java17-jdk-std", "java17-jre-distroless"]
}