variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "domain_name" {
  description = "The domain name to be used in the certificate"
  type        = string
}


variable "app_name" {
  description = "The app name to be used in the certificate"
  type        = string
}
