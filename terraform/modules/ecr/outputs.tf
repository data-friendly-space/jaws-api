output "ecr_repository_url" {
  value       = aws_ecr_repository.jaws_ecr.repository_url
  description = "The ECR's URL"
}