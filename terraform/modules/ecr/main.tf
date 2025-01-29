resource "aws_ecr_repository" "jaws_ecr" {
  name = var.ecr_name

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(var.tags, {
    Name        = "${var.ecr_name}"
    Environment = var.environment
    }
  )
}
