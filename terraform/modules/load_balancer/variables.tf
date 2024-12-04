variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}
variable "app_name" {
  description = "Value of app name"
  type        = string
}

variable "it_public_subnets" {
  description = "List of public subnets"
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "To get the security group ID from module security_group"
  type        = string
}

variable "idle_timeout" {
  description = "Value of idle timeout"
  type        = number
  default     = 30
}