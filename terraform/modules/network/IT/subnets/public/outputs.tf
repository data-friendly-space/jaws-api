output "ids" {
  description = "List of imported subnets"
  value       = [for subnet in data.aws_subnet.it_public_subnets : subnet.id]
}