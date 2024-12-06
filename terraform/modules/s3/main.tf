resource "aws_s3_bucket" "jaws-datasets-s3" {
  bucket = var.s3_datasets_name

  tags = merge(var.tags, {
    Name        = "${var.app_name}"
    Environment = var.environment
  })
}

resource "aws_s3_bucket_acl" "jaws-datasets-s3-acl"{
  bucket = aws_s3_bucket.jaws-datasets-s3.id
  acl    = "public-read"
}