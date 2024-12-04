output "vpc_id" {
  description = "The VPC ID"
  value       = data.aws_vpc.it_vpc.id
}