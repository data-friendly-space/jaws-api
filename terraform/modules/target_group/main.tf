
# aws_alb_target_group: Configures a group of targets (such as EC2 instances or containers) for the Application Load Balancer (ALB) to distribute traffic to.
# Defines the health checks used to determine the health of the targets.
resource "aws_alb_target_group" "alb" {
  name        = "${var.ecs_app_name}-tg"
  port        = var.ecs_container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = var.health_check_interval
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = var.health_check_timeout
    path                = var.health_check_endpoint
    unhealthy_threshold = "3"
  }

  tags = merge(var.tags, {
    Name = "${var.ecs_app_name}-tg"
    }
  )
}


resource "aws_alb_listener" "alb" {
  load_balancer_arn = var.load_balancer_alb_arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_alb_target_group.alb.arn
        weight = var.listerner_alb_tg_weight
      }
    }
  }

  tags = merge(var.tags, {
    Name = "alb-http-listener-${var.ecs_app_name}"
    }
  )
}


resource "aws_alb_listener_rule" "rule" {
  listener_arn = aws_alb_listener.alb.arn
  priority     = 1

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.alb.arn
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
  tags = merge(var.tags, {
    Name = "alb-listener-rule-${var.ecs_app_name}"
    }
  )
}