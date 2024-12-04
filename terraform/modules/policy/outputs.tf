output "ecs_execution_role_arn" {
  description = "Outputs policy ARN to attach on ecs roles"
  value       = data.aws_iam_role.ecs_execution_role.arn
}