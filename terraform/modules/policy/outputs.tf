output "ecs_execution_role_arn" {
  description = "Outputs policy ARN to attach on ecs roles"
  value       = aws_iam_role.ecs_execution_role.arn
}