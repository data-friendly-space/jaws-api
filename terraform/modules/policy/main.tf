resource "aws_iam_role" "ecs_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "policy_list_attachment" {
  for_each    = toset([
    "arn:aws:iam::aws:policy/AmazonCognitoDeveloperAuthenticatedIdentities",
    "arn:aws:iam::aws:policy/AmazonCognitoPowerUser",
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
  ])
  role        = aws_iam_role.ecs_execution_role.name
  policy_arn  = each.value
}

resource "aws_iam_role_policy_attachment" "cloudwatchlogcreation_policy_attach" {
  policy_arn = aws_iam_policy.CloudwatchLogCreation.arn
  role        = aws_iam_role.ecs_execution_role.name
}


resource "aws_iam_policy" "CloudwatchLogCreation" {
  name        = "CloudwatchLogCreation"
  path        = "/"
  policy = jsonencode(
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:ListTagsLogGroup",
                "logs:GetLogRecord",
                "logs:DeleteSubscriptionFilter",
                "logs:DescribeLogStreams",
                "logs:DescribeSubscriptionFilters",
                "logs:StartQuery",
                "logs:DescribeMetricFilters",
                "logs:DeleteLogStream",
                "logs:GetLogDelivery",
                "logs:ListLogDeliveries",
                "logs:CreateExportTask",
                "logs:CreateLogStream",
                "logs:DeleteMetricFilter",
                "logs:CancelExportTask",
                "logs:DeleteRetentionPolicy",
                "logs:GetLogEvents",
                "logs:DeleteLogDelivery",
                "logs:AssociateKmsKey",
                "logs:FilterLogEvents",
                "logs:DescribeQueryDefinitions",
                "logs:PutDestination",
                "logs:DescribeResourcePolicies",
                "logs:DescribeDestinations",
                "logs:DescribeQueries",
                "logs:DisassociateKmsKey",
                "logs:DescribeLogGroups",
                "logs:DeleteLogGroup",
                "logs:PutDestinationPolicy",
                "logs:StopQuery",
                "logs:TestMetricFilter",
                "logs:DeleteQueryDefinition",
                "logs:PutQueryDefinition",
                "logs:DeleteDestination",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:PutMetricFilter",
                "logs:CreateLogDelivery",
                "logs:DescribeExportTasks",
                "logs:GetQueryResults",
                "logs:UpdateLogDelivery",
                "logs:PutSubscriptionFilter",
                "logs:PutRetentionPolicy",
                "logs:GetLogGroupFields",
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "*"
        }
    ]
  })
  tags = merge(var.tags, {})
}



