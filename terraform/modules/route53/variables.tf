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

variable "company_asset_zone_name" {
  description = "Hosted zone name"
  type        = string
}