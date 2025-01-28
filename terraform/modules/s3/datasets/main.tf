resource "aws_s3_bucket" "jaws-datasets-s3" {
  bucket = var.s3_datasets_name

  tags = merge(var.tags, {
    Name        = "${var.app_name}"
    Environment = var.environment
  })
}

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
