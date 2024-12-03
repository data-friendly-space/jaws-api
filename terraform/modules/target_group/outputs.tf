output "alb_target_group_arn" {
  description = "The ARN of ALB target group"
  value       = aws_alb_target_group.alb.arn
}

output "alb_listener_arn" {
  description = "The ARN of ALB listener"
  value       = aws_alb_listener.alb.arn
}
