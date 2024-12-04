output "ecs_task_definition_arn" {
  description = "The Amazon Resource Name (ARN) of the ECS task definition"
  value       = aws_ecs_task_definition.task_definition.arn
}

output "ecs_service_arn" {
  description = "The Amazon Resource Name (ARN) of the ECS service"
  value       = aws_ecs_service.service.id
}

output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = aws_ecs_service.service.name
}

output "aws_cloudwatch_log_group_name" {
  description = "Cloudwatch log group name"
  value       = aws_cloudwatch_log_group.main.name  
}
