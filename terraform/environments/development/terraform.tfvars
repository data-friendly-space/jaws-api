#-------------------------------COMMON VARIABLES--------------------------
aws_region  = "us-east-1"
aws_profile = "default"
environment = "development"
tags = {
  "Project"     = "jaws"
  "Environment" = "development"
  "Managedby"   = "Terraform"
}

#-------------------------------NETWORK VARIABLES--------------------------
vpc_cidr_block = "172.31.0.0/16"
vpc_id         = "vpc-0fb5296d13dac730f"
vpc_name       = ""
#api_gateway_name        = "msa-api-gateway"
#api_gateway_description = "MyStoneridge API Gateway"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
it_public_subnets  = ["subnet-0c9afffe03d980eb3", "subnet-0ae19062beb00ca2a", "subnet-0c70a29289e1ceae1"]
it_public_subnet   = "subnet-0c9afffe03d980eb3"

zone_name = "jawsdev.com"
company_asset_zone_name = ""
#domain_name           = "*.my.stoneridge.app"
#api_default_stage_url = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com"
#api_v1_stage_url      = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com/v1"
#api_v2_stage_url      = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com/v2"

#-------------------------------jaws-service VARIABLES--------------------------
jaws_service_cluster_name                  = "jaws"
jaws_service_ecs_app_name                  = "jaws-service"
ecs_jaws_service_container_image           = "669246429926.dkr.ecr.us-east-1.amazonaws.com/jaws-dev:1"
ecs_jaws_service_container_name            = "jaws-service"
ecs_jaws_service_task_family               = "jaws-service-ecs-app"
ecs_jaws_service_container_port            = 80
ecs_jaws_service_container_memory          = 1024
ecs_jaws_service_container_cpu             = 512
ecs_jaws_service_desired_count             = 1
jaws_service_health_check_endpoint         = "/api/health"
jaws_service_ecs_health_check_grace_period = 120
jaws_service_health_check_interval         = 15
jaws_service_health_check_timeout          = 10
jaws_service_aws_cloudwatch_retention_days  = 7

