output "cluster_arn" {
  description = "The Amazon Resource Name (ARN) of the ECS cluster"
  value       = aws_ecs_cluster.cluster.arn
}

output "cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.cluster.name
}

output "cluster_id" {
  description = "The ID of the ECS cluster"
  value       = aws_ecs_cluster.cluster.id
}
