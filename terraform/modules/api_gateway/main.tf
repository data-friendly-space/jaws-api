
resource "aws_apigatewayv2_api" "msa" {
  name          = "MyStoneridgeApiGateway"
  protocol_type = "HTTP"
  tags          = var.tags
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.msa.id
  name        = "$default"
  auto_deploy = true
  tags        = var.tags
}

resource "aws_apigatewayv2_stage" "v1" {
  api_id      = aws_apigatewayv2_api.msa.id
  description = "Version 1"
  name        = "v1"
  auto_deploy = false
  tags        = var.tags
}

resource "aws_apigatewayv2_stage" "v2" {
  api_id      = aws_apigatewayv2_api.msa.id
  description = "Version 2"
  name        = "v2"
  auto_deploy = false
  tags        = var.tags
}

resource "aws_apigatewayv2_route" "activation_work_order" {
  api_id    = aws_apigatewayv2_api.msa.id
  route_key = "POST /activation/work-order"
}

resource "aws_apigatewayv2_route" "activation_work_order_status_g" {
  api_id    = aws_apigatewayv2_api.msa.id
  route_key = "GET /activation/work-order/status"
}

resource "aws_apigatewayv2_route" "activation_work_order_status_p" {
  api_id    = aws_apigatewayv2_api.msa.id
  route_key = "PUT /activation/work-order/status"
}

resource "aws_apigatewayv2_route" "activation_work_order_status_assetid_g" {
  api_id    = aws_apigatewayv2_api.msa.id
  route_key = "GET /activation/work-order/status/{assetId}"
}

resource "aws_apigatewayv2_route" "activation_work_order_list_by" {
  api_id    = aws_apigatewayv2_api.msa.id
  route_key = "GET /activation/work-order/list-by/asset/{Id}"
}

resource "aws_apigatewayv2_route" "activation_work_order_submit" {
  api_id    = aws_apigatewayv2_api.msa.id
  route_key = "PUT /activation/work-order/submit"
}