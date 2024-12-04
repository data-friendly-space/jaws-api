resource "aws_security_group" "alb" {
  name   = "${var.app_name}-sg"
  description = "Security group for loadbalancer to services on ECS"
  vpc_id = var.vpc_id

  ingress {
    protocol    = -1
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.app_name}-sg"
    }
  )
}