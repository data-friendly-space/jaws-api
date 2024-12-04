variable "environment" {
  description = "The environment for the resources"
  type        = string
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "vpc_id" {
  description = "The VPC ID for the network"
  type        = string
}

variable "app_name" {
  description = "The name of the application."
  type        = string
}

variable "vpc_cidr_block" {
  description = "VPC CIDR block"
  type        = string
}