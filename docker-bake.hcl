variable "DOCKER_REGISTRY" {
  default = "docker.io/taha2samy"
}

variable "GHCR_REGISTRY" {
  default = "ghcr.io/taha2samy"
}

variable "REPO_DOCKER" {
  default = "java"
}

variable "REPO_GHCR" {
  default = "java"
}

variable "CACHE_TAG" {
  default = "cache"
}

target "_common" {
  platforms = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=registry,ref=${DOCKER_REGISTRY}/${REPO_DOCKER}:${CACHE_TAG}"]
  cache-to   = ["type=registry,ref=${DOCKER_REGISTRY}/${REPO_DOCKER}:${CACHE_TAG},mode=min"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]

}

group "java8" {
  targets = ["java8-jre-std", "java8-jdk-std", "java8-jre-distroless"]
}

group "java11" {
  targets = ["java11-jre-std", "java11-jdk-std", "java11-jre-distroless"]
}

group "java17" {
  targets = ["java17-jre-std", "java17-jdk-std", "java17-jre-distroless"]
}

group "java21" {
  targets = ["java21-jre-std", "java21-jdk-std", "java21-jre-distroless"]
}
group "java25" {
  targets = ["java25-jre-std", "java25-jdk-std", "java25-jre-distroless"]
}

