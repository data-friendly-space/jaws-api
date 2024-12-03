data "template_file" "container_definition_env" {
  template = "${file("./environments/${var.environment}/${var.ecs_app_name}/container_definition.tftpl")}"

  vars = {
    container_name            = var.container_name
    container_image           = var.container_image
    container_memory          = var.container_memory
    container_cpu             = var.container_cpu
    container_port            = var.container_port
    aws_cloudwatch_log_group  = var.aws_cloudwatch_log_group
    region                    = var.region
  }
}

resource "aws_ecs_task_definition" "task_definition" {
  family                   = var.task_family
  execution_role_arn       = var.ecs_execution_role_arn #aws_iam_role.ecs_execution_role.arn
  task_role_arn            = var.ecs_execution_role_arn #aws_iam_role.ecs_execution_role.arn
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.container_cpu
  memory                   = var.container_memory

  container_definitions = data.template_file.container_definition_env.rendered

  tags = merge(var.tags, {
    Name        = "${var.ecs_app_name}"
    Environment = var.environment
  })
}

resource "aws_ecs_service" "service" {
  name                               = "${var.ecs_app_name}"
  cluster                            = var.cluster_id #aws_ecs_cluster.cluster.id
  task_definition                    = aws_ecs_task_definition.task_definition.arn
  health_check_grace_period_seconds  = var.ecs_health_check_grace_period
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200
  desired_count                      = var.desired_count
  launch_type                        = "FARGATE"
  scheduling_strategy                = "REPLICA"

  network_configuration {
    subnets          = var.subnet_ids
    assign_public_ip = true
    security_groups  = [var.security_group_id]
  }

  load_balancer {
    target_group_arn = var.aws_alb_target_group_arn
    container_name   = "${var.container_name}"
    container_port   = var.container_port
  }

  deployment_controller {
    type = "ECS"
  }

  deployment_circuit_breaker {
    enable   = var.deployment_circuit_breaker_value
    rollback = var.deployment_circuit_breaker_value
  }

  depends_on = [
    aws_ecs_task_definition.task_definition
  ]

  lifecycle {
    ignore_changes = [
      task_definition
    ]
  }



  tags = merge(var.tags, {
    Name        = "${var.ecs_app_name}"
    Environment = var.environment
  })
}

//Todo: Move to a module
resource "aws_cloudwatch_log_group" "main" {
  name              = "/ecs/${var.ecs_app_name}"
  retention_in_days = var.aws_cloudwatch_retention_days

  tags = merge(var.tags, {
    Name        = "cloudwatch-log-task-${var.ecs_app_name}"
    Environment = var.environment
  })
}

//Todo:Move to a module
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 5
  min_capacity       = var.desired_count
  resource_id        = "service/${var.cluster_name}/${aws_ecs_service.service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ecs_policy_memory" {
  name               = "${var.ecs_app_name}-memory-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }

    target_value       = 80
    scale_in_cooldown  = 300
    scale_out_cooldown = 300
  }
}

resource "aws_appautoscaling_policy" "ecs_policy_cpu" {
  name               = "${var.ecs_app_name}-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 60
    scale_in_cooldown  = 300
    scale_out_cooldown = 300
  }
}

