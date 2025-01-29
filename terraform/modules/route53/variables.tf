variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "environment" {
  type = string
}

variable "zone_name" {
  description = "The name of the hosted zone."
  type        = string
}

variable "comment" {
  description = "Comment for the route 53"
  type        = string
}

variable "app_name" {
  description = "Application name"
  type        = string
}

variable "frontend_bucket_id" {
  description = "The bucket id of the frontend"
  type        = string
}