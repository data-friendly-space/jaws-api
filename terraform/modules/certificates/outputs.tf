output "certificate_arn" {
  description = "The ARN of the SSL certificate"
  value       = aws_acm_certificate.cert.arn
}

output "zone_id" {
  value = data.aws_route53_zone.existing.zone_id
}

output "fqdn" {
  value = aws_route53_record.cert_validation.fqdn
}

output "domain_name" {
  value = aws_acm_certificate.cert.domain_name
}
