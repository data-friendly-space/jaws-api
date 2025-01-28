variable "tags" {
  description = "Resource Tags"
  type        = map(string)
  default     = {}
}
variable "environment" {
  description = "Environment's name"
  type        = string
}

variable "ecr_name" {
  description = "ECR name"
  type        = string
}

