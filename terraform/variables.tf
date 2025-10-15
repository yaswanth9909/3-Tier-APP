variable "profile" {
  type    = string
  default = "three-tier"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "cluster_name" {
  type    = string
  default = "three-tier-eks"
}

variable "desired_size" {
  type    = number
  default = 2
}

variable "min_size" {
  type    = number
  default = 2
}

variable "max_size" {
  type    = number
  default = 4
}

variable "node_instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}

# Lock down who can hit the public API (your workstation IP /32).
# You can add more CIDRs if needed.
variable "public_api_cidrs" {
  type    = list(string)
  default = ["0.0.0.0/0"] # replace with ["YOUR.IP.ADDR.ESS/32"] for tighter access
}



