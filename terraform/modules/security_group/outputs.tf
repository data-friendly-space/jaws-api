output "alb_security_group_id" {
  description = "Application Load Balancer security group ID"
  value       = aws_security_group.alb.id
}