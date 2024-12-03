resource "aws_vpc" "it_vpc" {
  cidr_block = var.vpc_cidr_block
  lifecycle {
    prevent_destroy = true
  }
}