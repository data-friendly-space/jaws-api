provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

terraform {
  backend "s3" {
    key     = "jaws.terraform.tfstate"
    region  = "us-east-1"
    profile = "default"
    encrypt = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
  }
}

##---------------------- MODULES DECLARATION --------------------------##
##---------------------- NETWORK DECLARATION --------------------------##
module "network_it_vpc" {
  source         = "./modules/network/IT/vpcs"
  vpc_cidr_block = var.vpc_cidr_block
  vpc_name       = var.vpc_name
  vpc_id         = var.vpc_id
}

#module "it_private_subnets" {
#  source = "./modules/network/IT/subnets/private"
#  private_subnet_ids = var.it_private_subnets
#}

module "it_public_subnets" {
  source = "./modules/network/IT/subnets/public"

  public_subnet_ids = var.it_public_subnets
}



module "policy" {
  source = "./modules/policy"
  tags   = var.tags
}
