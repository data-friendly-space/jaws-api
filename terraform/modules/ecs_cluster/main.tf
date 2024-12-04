resource "aws_ecs_cluster" "cluster" {
  name = "${var.cluster_name}"

  tags = merge(var.tags, {
    Name        = "${var.cluster_name}"
    Environment = var.environment
    }
  )
}