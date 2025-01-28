resource "aws_iam_role" "ecs_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement : [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

}

resource "aws_iam_role_policy_attachment" "policy_list_attachment" {
  for_each = toset([
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
  ])
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = each.value
}

resource "aws_iam_role_policy_attachment" "cloudwatchlogcreation_policy_attach" {
  policy_arn = aws_iam_policy.CloudwatchLogCreation.arn
  role       = aws_iam_role.ecs_execution_role.name
}


resource "aws_iam_policy" "CloudwatchLogCreation" {
  name = "CloudwatchLogCreation"

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "VisualEditor0",
          "Effect" : "Allow",
          "Action" : [
            "logs:GetDataProtectionPolicy",
            "logs:GetLogRecord",
            "logs:DeleteSubscriptionFilter",
            "secretsmanager:DescribeSecret",
            "logs:DescribeSubscriptionFilters",
            "logs:StartQuery",
            "logs:DescribeMetricFilters",
            "logs:ListLogDeliveries",
            "secretsmanager:GetRandomPassword",
            "logs:CreateLogStream",
            "logs:CancelExportTask",
            "logs:DeleteRetentionPolicy",
            "logs:GetLogEvents",
            "logs:FilterLogEvents",
            "logs:DescribeDestinations",
            "logs:PutDataProtectionPolicy",
            "logs:Unmask",
            "logs:StopQuery",
            "logs:DeleteQueryDefinition",
            "logs:CreateLogGroup",
            "logs:ListTagsForResource",
            "logs:Link",
            "logs:CreateLogDelivery",
            "logs:PutMetricFilter",
            "logs:DescribeExportTasks",
            "logs:GetQueryResults",
            "logs:UpdateLogDelivery",
            "logs:PutSubscriptionFilter",
            "logs:ListTagsLogGroup",
            "logs:DeleteDataProtectionPolicy",
            "logs:DescribeLogStreams",
            "logs:GetLogDelivery",
            "logs:DeleteLogStream",
            "secretsmanager:ListSecretVersionIds",
            "logs:CreateExportTask",
            "logs:DeleteMetricFilter",
            "secretsmanager:GetSecretValue",
            "logs:AssociateKmsKey",
            "logs:DeleteLogDelivery",
            "logs:DescribeQueryDefinitions",
            "logs:DescribeResourcePolicies",
            "logs:PutDestination",
            "logs:DescribeQueries",
            "logs:DisassociateKmsKey",
            "logs:DescribeLogGroups",
            "logs:DeleteLogGroup",
            "logs:PutDestinationPolicy",
            "logs:TestMetricFilter",
            "logs:PutQueryDefinition",
            "logs:DeleteDestination",
            "logs:PutLogEvents",
            "secretsmanager:GetResourcePolicy",
            "logs:PutRetentionPolicy",
            "logs:GetLogGroupFields"
          ],
          "Resource" : "*"
        }
      ]
    }
  )
}
