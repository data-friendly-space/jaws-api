locals {
  count = length(var.public_subnet_ids)
}

data "aws_subnet" "it_public_subnets" {
  for_each = toset(var.public_subnet_ids)

  id = each.value
}