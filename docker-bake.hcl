variable "REGISTRY" {
  default = "ghcr.io/specter-stack"
}

variable "WOLFI_BASE_DIGEST" {
  default = "latest"
}

variable "WOLFI_STATIC_DIGEST" {
  default = "latest"
}

target "_common" {
  platforms = ["linux/amd64", "linux/arm64"]
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