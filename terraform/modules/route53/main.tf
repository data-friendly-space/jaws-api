resource "aws_route53_zone" "main" {
  name    = var.zone_name
  comment = var.comment
  tags    = var.tags
}

resource "aws_route53_zone" "company_asset" {
  name    = var.company_asset_zone_name
  comment = var.comment
  tags    = var.tags

}

