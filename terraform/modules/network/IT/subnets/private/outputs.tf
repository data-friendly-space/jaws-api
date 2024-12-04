output "ids" {
  description = "List of imported private subnets"
  value       = [for subnet in data.aws_subnet.it_private_subnets : subnet.id]
}