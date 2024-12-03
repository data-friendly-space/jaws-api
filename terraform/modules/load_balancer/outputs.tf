output "alb_arn" {
  description = "Application Load Balancer arn ID"
  value       = aws_lb.alb.arn
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = aws_lb.alb.dns_name
}


