##------------------- COMMON VARIABLES ----------------##             
variable "aws_region" {
  description = "Default AWS Region"
  type        = string
}

variable "aws_profile" {
  description = "Account's Profile"
  type        = string
}

variable "tags" {
  description = "A mapping of tags to assign to all resources"
  type        = map(string)
  default     = {}

}

variable "environment" {
  description = "Environment's name"
  type        = string
}

variable "availability_zones" {
  description = "List of AZs"
  type        = list(string)
}

##------------------- NETWORK VARIABLES ----------------## 
variable "vpc_cidr_block" {
  description = "The CIDR block for the VPC"
  type        = string
}

variable "vpc_name" {
  description = "The name of the VPC"
  type        = string
}

variable "vpc_id" {
  description = "The id of the VPC"
  type        = string
}


variable "it_public_subnets" {
  description = "List of public subnets, created by IT team"
  type        = list(string)
}

variable "it_public_subnet" {
  description = "A public subnet, created by IT team"
  type        = string
}

variable "zone_name" {
  description = "Zone name for Route53"
  type        = string
}



##------------------- SERVICES VARIABLES ----------------##   


##------------------- price-ai-service VARIABLES ----------------##
variable "price_ai_service_cluster_name" {
  description = "The price-ai cluster name"
  type        = string
}

variable "ecs_price_ai_service_task_family" {
  description = "ECS task family"
  type        = string
}

variable "ecs_price_ai_service_container_name" {
  description = "Value of container name"
  type        = string
}

variable "ecs_price_ai_service_container_image" {
  description = "Value of container image"
  type        = string
}

variable "ecs_price_ai_service_container_port" {
  description = "Container port number"
  type        = number
}

variable "ecs_price_ai_service_container_memory" {
  description = "Container memory size"
  type        = number
}

variable "ecs_price_ai_service_container_cpu" {
  description = "Container cpu size"
  type        = number
}

variable "ecs_price_ai_service_desired_count" {
  description = "Desired count value"
  type        = number
}

variable "price_ai_service_ecs_app_name" {
  description = "App name"
  type        = string
}

variable "price_ai_service_health_check_endpoint" {
  description = "Health check path"
  type        = string
}

variable "price_ai_service_health_check_interval" {
  description = "Value of health check interval"
  type        = number
}
variable "price_ai_service_health_check_timeout" {
  description = "Value of health check timeout"
  type        = number
}

variable "price_ai_service_ecs_health_check_grace_period" {
  description = "Service grace period value"
  type        = number
}

variable "price_ai_service_aws_cloudwatch_retention_days" {
  description = "Cloudwatch retention in days"
  type        = number
}