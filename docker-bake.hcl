variable "GHCR_REGISTRY" {
  default = "ghcr.io/taha2samy"
}

variable "REPO_GHCR" {
  default = "java"
}

target "_common" {
  platforms = ["linux/amd64", "linux/arm64"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]
  output = ["type=registry,compression=zstd,compression-level=3,force-compression=true"]
  args = {
    KEYSTORE_PWD = "changeit"
  }
}

group "default" {
  targets = ["java8", "java11", "java17", "java21", "java25"]
}


