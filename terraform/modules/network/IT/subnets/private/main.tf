locals {
  count = length(var.private_subnet_ids)
}

data "aws_subnet" "it_private_subnets" {
  for_each = toset(var.private_subnet_ids)

  id = each.value
}