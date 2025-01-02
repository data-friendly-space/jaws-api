resource "aws_s3_bucket" "jaws-datasets-s3" {
  bucket = var.s3_datasets_name

  tags = merge(var.tags, {
    Name        = "${var.app_name}"
    Environment = var.environment
  })
}

# resource "aws_s3_bucket_public_access_block" "jaws-datasets-s3-public-access-block" {
#   bucket = aws_s3_bucket.jaws-datasets-s3.id

#   block_public_acls       = false
#   block_public_policy     = false
#   ignore_public_acls      = false
#   restrict_public_buckets = false
# }

# resource "aws_s3_bucket_acl" "jaws-datasets-s3-acl" {
#   bucket = aws_s3_bucket.jaws-datasets-s3.id
#   acl    = "public-read"
# }
resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.jaws-datasets-s3.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.jaws-datasets-s3.arn}/*"
      }
    ]
  })
}
