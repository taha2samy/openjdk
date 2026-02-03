variable "REGISTRY" {
  default = "docker.io/taha2samy"
}


target "_common" {
  platforms = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=registry,ref=${REGISTRY}/openjdk:${CACHE_TAG}"]
  cache-to   = ["type=registry,ref=${REGISTRY}/openjdk:${CACHE_TAG},mode=max"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]

}

group "java17" {
  targets = ["java17-jre-std", "java17-jdk-std", "java17-jre-distroless"]
}