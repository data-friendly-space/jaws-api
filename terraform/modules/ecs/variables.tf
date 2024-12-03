variable "cluster_id" {
  description = "The ID of the ECS cluster to create"
  type        = string
}


variable "cluster_name" {
  description = "The name of the ECS cluster to create"
  type        = string
}

variable "task_family" {
  description = "The name of the task family for the ECS service"
  type        = string
}

variable "container_name" {
  description = "The Docker image to run in the ECS service"
  type        = string
}

variable "container_image" {
  description = "The Docker image to run in the ECS service"
  type        = string
}

variable "container_port" {
  description = "The port to expose in the Docker container"
  type        = number
}

variable "host_port" {
  description = "The port to expose in the host"
  type        = number
  default     = 80
}

variable "container_memory" {
  description = "The amount of memory to allocate to the container"
  type        = number
}

variable "container_cpu" {
  description = "The amount of CPU to allocate to the container"
  type        = number
}

variable "desired_count" {
  description = "The desired number of tasks to run in the ECS service"
  type        = number
}

variable "security_group_id" {
  description = "The ID of the security group to attach to the ECS service"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "environment" {
  type = string
}

variable "subnet_ids" {
  description = "A list of VPC subnet IDs to launch the service in"
  type        = list(string)
}

variable "aws_alb_target_group_arn" {
  type = string
}

variable "region" {
  type = string
}

variable "ecs_app_name" {
  description = "The name of the ECS application."
  type        = string
}

variable "ecs_health_check_grace_period" {
  description = "Grace Period value of service"
  type        = number
  default     = 60
}

variable "log_group_retention" {
  description = "Retention in days for CloudWatch log group"
  type        = number
  default     = 14
}

variable "aws_cloudwatch_log_group" {
  description = "Log group name"
  type        = string
}

variable "aws_cloudwatch_retention_days" {
  description = "Retention days"
  type        = number
  default     = 30
}

variable "deployment_circuit_breaker_value" {
  description = "Bolean Value"
  type        = bool
  default     = false 
}

variable "ecs_execution_role_arn" {
  description = "Gets outputs from ecs_role in policy module"
  type        = string 
}
