resource "aws_resourcegroups_group" "resource_group" {
  name = "${var.app_name}"

  resource_query {
    query = jsonencode({
      ResourceTypeFilters = [
        "AWS::AllSupported",
      ],
      TagFilters = [
        {
          Key    = "Environment",
          Values = [var.environment]
        },
        {
          Key    = "App",
          Values = [var.app_name]
        }
      ]
    })
  }
}
