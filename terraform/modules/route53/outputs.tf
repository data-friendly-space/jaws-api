output "hosted_zone_id" {
  value = aws_route53_zone.main.id
}

output "name_servers" {
  value = aws_route53_zone.main.name_servers
}