data "aws_route53_zone" "main" {
  zone_id = var.route53_zone_id
}

resource "aws_acm_certificate" "cert" {
  domain_name       = "*.${data.aws_route53_zone.main.name}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(var.tags, {
    Name        = "${var.environment}-${data.aws_route53_zone.main.name}-cert"
    Environment = var.environment
  })
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      type   = dvo.resource_record_type
      value  = dvo.resource_record_value
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.value]
  type            = each.value.type
  zone_id         = data.aws_route53_zone.main.zone_id
  ttl             = 60

  depends_on = [aws_acm_certificate.cert]

}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
