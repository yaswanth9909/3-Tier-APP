terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.15.0, < 7.0.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
    tls       = { source = "hashicorp/tls", version = ">= 4.0.0" }
    null      = { source = "hashicorp/null", version = ">= 3.0.0" }
    time      = { source = "hashicorp/time", version = ">= 0.9.0" }
    cloudinit = { source = "hashicorp/cloudinit", version = ">= 2.0.0" }
  }
}