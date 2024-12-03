##---------------------- jaws-service DECLARATION --------------------------##
module "ecs_cluster_jaws_service" {
  source = "./modules/ecs_cluster"

  cluster_name = var.jaws_service_cluster_name
  environment  = var.environment
  tags         = var.tags
}

module "ecs_jaws_service" {
  source = "./modules/ecs"

  cluster_name                  = var.jaws_service_cluster_name
  cluster_id                    = module.ecs_cluster_jaws_service.cluster_id
  task_family                   = var.ecs_jaws_service_task_family
  container_name                = var.ecs_jaws_service_container_name
  container_image               = var.ecs_jaws_service_container_image
  container_port                = var.ecs_jaws_service_container_port
  container_memory              = var.ecs_jaws_service_container_memory
  container_cpu                 = var.ecs_jaws_service_container_cpu
  desired_count                 = var.ecs_jaws_service_desired_count
  subnet_ids                    = module.it_public_subnets.ids
  security_group_id             = module.jaws_service_security_group.alb_security_group_id
  aws_alb_target_group_arn      = module.jaws_service_target_group.alb_target_group_arn
  ecs_health_check_grace_period = var.jaws_service_ecs_health_check_grace_period
  environment                   = var.environment
  tags                          = var.tags
  region                        = var.aws_region
  ecs_app_name                  = var.jaws_service_ecs_app_name
  aws_cloudwatch_log_group      = module.ecs_jaws_service.aws_cloudwatch_log_group_name
  aws_cloudwatch_retention_days = var.jaws_service_aws_cloudwatch_retention_days
  ecs_execution_role_arn        = module.policy.ecs_execution_role_arn
}

module "jaws_service_security_group" {
  source = "./modules/security_group"

  vpc_id         = var.vpc_id
  vpc_cidr_block = var.vpc_cidr_block
  app_name       = var.jaws_service_ecs_app_name
  environment    = var.environment
  tags           = var.tags
}

module "jaws_service_load_balancer" {
  source = "./modules/load_balancer"

  it_public_subnets     = module.it_public_subnets.ids
  app_name              = var.jaws_service_ecs_app_name
  alb_security_group_id = module.jaws_service_security_group.alb_security_group_id

}

module "jaws_service_target_group" {
  source = "./modules/target_group"

  vpc_id                = var.vpc_id
  ecs_app_name          = var.jaws_service_ecs_app_name
  ecs_container_port    = var.ecs_jaws_service_container_port
  health_check_endpoint = var.jaws_service_health_check_endpoint
  health_check_interval = var.jaws_service_health_check_interval
  health_check_timeout  = var.jaws_service_health_check_timeout
  load_balancer_alb_arn = module.jaws_service_load_balancer.alb_arn
  enable_listener_80xx  = false
  environment           = var.environment
  tags                  = var.tags
}

module "jaws_service_resource_group" {
  source = "./modules/resource_group"

  app_name    = var.jaws_service_ecs_app_name
  environment = var.environment
  tags        = var.tags
}