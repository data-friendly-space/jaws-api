data "aws_lb" "alb" {
  name = "${var.app_name}-private-alb"
}

data "aws_s3_bucket" "frontend" {
  bucket = var.frontend_bucket_id
}

resource "aws_route53_zone" "main" {
  name    = var.zone_name
  comment = var.comment
  tags    = var.tags
}

resource "aws_route53_record" "frontend" {
  zone_id = aws_route53_zone.main.zone_id
  name    = format("%s%s", "frontend.", var.zone_name)
  type    = "A"

  alias {
    name                   = data.aws_s3_bucket.frontend.website_endpoint
    zone_id                = aws_route53_zone.main.zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = format("%s%s", "api.", var.zone_name)
  type    = "A"

  alias {
    name                   = data.aws_lb.alb.dns_name
    zone_id                = data.aws_lb.alb.zone_id
    evaluate_target_health = true
  }
}