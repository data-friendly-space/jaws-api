#-------------------------------COMMON VARIABLES--------------------------
aws_region  = "us-east-1"
aws_profile = "rxsense"
environment = "sandbox"
tags = {
  "Project"     = "price-ai"
  "Environment" = "sandbox"
  "Managedby"   = "Terraform"
}

#-------------------------------NETWORK VARIABLES--------------------------
vpc_cidr_block = "172.31.0.0/16"
vpc_id         = "vpc-0675535c93396341f"
vpc_name       = ""
#api_gateway_name        = "msa-api-gateway"
#api_gateway_description = "MyStoneridge API Gateway"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
it_public_subnets  = ["subnet-022c7b209f6defac3", "subnet-0b12359b76803f23e", "subnet-0a1fb35b0168e2739"]
it_public_subnet   = "subnet-022c7b209f6defac3"

zone_name = "rxsbnsdemo.com"
company_asset_zone_name = ""
#domain_name           = "*.my.stoneridge.app"
#api_default_stage_url = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com"
#api_v1_stage_url      = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com/v1"
#api_v2_stage_url      = "https://0bvlvjdqme.execute-api.us-west-2.amazonaws.com/v2"

#-------------------------------price-ai-service VARIABLES--------------------------
price_ai_service_cluster_name                  = "price-ai"
price_ai_service_ecs_app_name                  = "price-ai-service"
ecs_price_ai_service_container_image           = "484882625153.dkr.ecr.us-east-1.amazonaws.com/price-ai-service:latest"
ecs_price_ai_service_container_name            = "price-ai-service"
ecs_price_ai_service_task_family               = "price-ai-service-ecs-app"
ecs_price_ai_service_container_port            = 80
ecs_price_ai_service_container_memory          = 1024
ecs_price_ai_service_container_cpu             = 512
ecs_price_ai_service_desired_count             = 1
price_ai_service_health_check_endpoint         = "/api/health"
price_ai_service_ecs_health_check_grace_period = 120
price_ai_service_health_check_interval         = 15
price_ai_service_health_check_timeout          = 10
price_ai_service_aws_cloudwatch_retention_days  = 7

