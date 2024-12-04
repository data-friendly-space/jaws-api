variable "environment" {
  type = string
}

variable "tags" {
  description = "List of tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "app_name" {
  description = "Value of app name"
  type        = string
}