variable "tags" {
  description = "Resource Tags"
  type        = map(string)
  default     = {}
}
variable "environment" {
  description = "Environment's name"
  type        = string
}

variable "app_name" {
  description = "App name"
  type        = string
}

variable "bucket_name" {
  description = "Name of the bucket"
  type        = string
}

