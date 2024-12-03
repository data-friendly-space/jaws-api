variable "environment" {
  description = "The environment for the resources"
  type        = string
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "ecs_app_name" {
  description = "App Name"
  type        = string
}

variable "ecs_container_port" {
  description = "The port of ECS Container"
  type        = number
}

variable "vpc_id" {
  description = "VPC ID created by IT Team"
  type        = string
}

variable "health_check_endpoint" {
  description = "Path value of health check endpoint"
  type        = string
}
variable "health_check_interval" {
  description = "Value of health check interval"
  type        = number
  default     = 15
}
variable "health_check_timeout" {
  description = "Value of health check timeout"
  type        = number
  default     = 10
}


variable "load_balancer_alb_arn" {
  description = "to get the ALB arn value from module load_balancer"
  type        = string
}

variable "enable_listener_80xx" {
  description = "To set up specific listener for 808x ports"
  type        = bool
}


variable "listerner_alb_tg_weight" {
  description = "Weight value of alb listener target group"
  type        = number
  default     = 1
}