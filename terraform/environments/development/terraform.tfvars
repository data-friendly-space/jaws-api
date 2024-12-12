#-------------------------------COMMON VARIABLES--------------------------
aws_region  = "us-east-1"
aws_profile = "841162704359_ExternalDeveloper"
environment = "development"
tags = {
  "Project"     = "jaws"
  "Environment" = "development"
  "Managedby"   = "Terraform"
}

#-------------------------------NETWORK VARIABLES--------------------------
vpc_cidr_block = "172.31.0.0/16"
vpc_id         = "vpc-07dd783259aae3728"
vpc_name       = ""
#api_gateway_name        = "msa-api-gateway"
#api_gateway_description = "MyStoneridge API Gateway"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
it_public_subnets  = ["subnet-017b0144f753b8028", "subnet-0a1fa7026dc5ba396", "subnet-01dd0044f6a1c4bad"]
it_public_subnet   = "subnet-017b0144f753b8028"

zone_name               = "jawsdev.com"
company_asset_zone_name = ""
#domain_name           = "*.my.stoneridge.app"
#api_default_stage_url = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com"
#api_v1_stage_url      = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com/v1"
#api_v2_stage_url      = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com/v2"

#-------------------------------jaws-api VARIABLES--------------------------
jaws_api_cluster_name                  = "jaws"
jaws_api_ecs_app_name                  = "jaws-api"
jaws_s3_datasets_name                  = "jaws-datasets"
jaws_ecr_name                          = "jaws-ecr"
ecs_jaws_api_container_image           = "jaws-api:latest"
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

