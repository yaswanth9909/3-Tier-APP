output "cluster_name" { value = module.eks.cluster_name }
output "region" { value = var.region }
output "vpc_id" { value = module.vpc.vpc_id }
