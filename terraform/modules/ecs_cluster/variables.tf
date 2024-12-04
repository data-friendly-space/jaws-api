variable "tags" {
  description = "Resource Tags"
  type        = map(string)
  default     = {}
}
variable "environment" {
  description = "Environment's name"
  type        = string
}

variable "cluster_name" {
  description = "ECS Cluster name"
  type        = string
}

