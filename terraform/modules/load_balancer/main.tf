resource "aws_lb" "alb" {
  name                       = "${var.app_name}-private-alb"
  internal                   = true
  load_balancer_type         = "application"
  security_groups            = [var.alb_security_group_id]
  subnets                    = var.it_public_subnets ###
  enable_deletion_protection = false
  idle_timeout               = var.idle_timeout

  tags = merge(var.tags, {
    Name = "${var.app_name}-private-alb"
    }
  )
}
