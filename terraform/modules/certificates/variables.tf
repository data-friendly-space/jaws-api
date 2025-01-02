variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "route53_zone_id" {
  description = "Id of the route53 zone"
  type        = string
}


variable "app_name" {
  description = "The app name to be used in the certificate"
  type        = string
}
