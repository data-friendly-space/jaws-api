##---------------------- jaws-api DECLARATION --------------------------##
module "ecs_cluster_jaws_api" {
  source = "./modules/ecs_cluster"

  cluster_name = var.jaws_api_cluster_name
  environment  = var.environment
  tags         = var.tags
}

module "ecs_jaws_api" {
  source = "./modules/ecs"

  cluster_name                  = var.jaws_api_cluster_name
  cluster_id                    = module.ecs_cluster_jaws_api.cluster_id
  task_family                   = var.ecs_jaws_api_task_family
  container_name                = var.ecs_jaws_api_container_name
  container_image               = var.ecs_jaws_api_container_image
  container_port                = var.ecs_jaws_api_container_port
  container_memory              = var.ecs_jaws_api_container_memory
  container_cpu                 = var.ecs_jaws_api_container_cpu
  desired_count                 = var.ecs_jaws_api_desired_count
  subnet_ids                    = module.it_public_subnets.ids
  security_group_id             = module.jaws_api_security_group.alb_security_group_id
  aws_alb_target_group_arn      = module.jaws_api_target_group.alb_target_group_arn
  ecs_health_check_grace_period = var.jaws_api_ecs_health_check_grace_period
  environment                   = var.environment
  tags                          = var.tags
  region                        = var.aws_region
  ecs_app_name                  = var.jaws_api_ecs_app_name
  aws_cloudwatch_log_group      = module.ecs_jaws_api.aws_cloudwatch_log_group_name
  aws_cloudwatch_retention_days = var.jaws_api_aws_cloudwatch_retention_days
  ecs_execution_role_arn        = module.policy.ecs_execution_role_arn
}

module "jaws_api_security_group" {
  source = "./modules/security_group"

  vpc_id         = var.vpc_id
  vpc_cidr_block = var.vpc_cidr_block
  app_name       = var.jaws_api_ecs_app_name
  environment    = var.environment
  tags           = var.tags
}

module "jaws_api_load_balancer" {
  source = "./modules/load_balancer"

  it_public_subnets     = module.it_public_subnets.ids
  app_name              = var.jaws_api_ecs_app_name
  alb_security_group_id = module.jaws_api_security_group.alb_security_group_id

}

module "jaws_api_target_group" {
  source = "./modules/target_group"

  vpc_id                = var.vpc_id
  ecs_app_name          = var.jaws_api_ecs_app_name
  ecs_container_port    = var.ecs_jaws_api_container_port
  health_check_endpoint = var.jaws_api_health_check_endpoint
  health_check_interval = var.jaws_api_health_check_interval
  health_check_timeout  = var.jaws_api_health_check_timeout
  load_balancer_alb_arn = module.jaws_api_load_balancer.alb_arn
  enable_listener_80xx  = false
  environment           = var.environment
  tags                  = var.tags
}

module "jaws_api_resource_group" {
  source = "./modules/resource_group"

  app_name    = var.jaws_api_ecs_app_name
  environment = var.environment
  tags        = var.tags
}