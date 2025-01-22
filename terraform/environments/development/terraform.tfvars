#-------------------------------COMMON VARIABLES--------------------------
aws_region  = "us-east-1"
aws_profile = "jaws-dfs"
environment = "development"
tags = {
  "project"     = "jaws"
  "Environment" = "development"
  "Managedby"   = "Terraform"
}

#-------------------------------NETWORK VARIABLES--------------------------
vpc_cidr_block = "172.31.0.0/16"
vpc_id         = "vpc-07dd783259aae3728"
vpc_name       = ""

availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
it_public_subnets  = ["subnet-017b0144f753b8028", "subnet-0a1fa7026dc5ba396", "subnet-01dd0044f6a1c4bad"]
it_public_subnet   = "subnet-017b0144f753b8028"

zone_name    = "jawsdev.thedeep.io"
zone_comment = "Jaws development domain"

#-------------------------------jaws-api VARIABLES--------------------------
jaws_api_cluster_name                  = "jaws"
jaws_api_ecs_app_name                  = "jaws-api"
jaws_s3_datasets_name                  = "jaws-dataset"
jaws_ecr_name                          = "jaws-ecr"
ecs_jaws_api_container_image           = "latest"
ecs_jaws_api_container_name            = "jaws-api"
ecs_jaws_api_task_family               = "jaws-api-ecs-app"
ecs_jaws_api_container_port            = 80
ecs_jaws_api_container_memory          = 1024
ecs_jaws_api_container_cpu             = 512
ecs_jaws_api_desired_count             = 1
jaws_api_health_check_endpoint         = "/api/health"
jaws_api_ecs_health_check_grace_period = 120
jaws_api_health_check_interval         = 15
jaws_api_health_check_timeout          = 10
jaws_api_aws_cloudwatch_retention_days = 7

