data "aws_iam_role" "ecs_execution_role" {
  name = "ecsTaskExecutionRole"
}

resource "aws_iam_role_policy_attachment" "policy_list_attachment" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonCognitoDeveloperAuthenticatedIdentities",
    "arn:aws:iam::aws:policy/AmazonCognitoPowerUser",
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
  ])
  role       = data.aws_iam_role.ecs_execution_role.name
  policy_arn = each.value
}

resource "aws_iam_role_policy_attachment" "cloudwatchlogcreation_policy_attach" {
  policy_arn = data.aws_iam_policy.CloudwatchLogCreation.arn
  role       = data.aws_iam_role.ecs_execution_role.name
}


data "aws_iam_policy" "CloudwatchLogCreation" {
  name = "CloudwatchLogCreation"
}



