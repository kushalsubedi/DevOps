# CORS Handler Lambda Function
resource "aws_lambda_function" "cors_handler" {
  function_name = "CORSHandler"
  filename      = "${path.module}/lambda/cors_handler.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/cors_handler.zip")
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "cors_handler.lambda_handler"
  runtime       = "python3.12"
}

# API Gateway Integration for CORS
resource "aws_apigatewayv2_integration" "cors_integration" {
  api_id           = aws_apigatewayv2_api.upload_api.id
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  integration_uri  = aws_lambda_function.cors_handler.invoke_arn
  payload_format_version = "2.0"
}

# Lambda Permission for CORS Handler
resource "aws_lambda_permission" "allow_cors" {
  statement_id  = "AllowCORS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cors_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}

# OPTIONS routes for all POST endpoints
resource "aws_apigatewayv2_route" "delete_options" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "OPTIONS /delete-file"
  target    = "integrations/${aws_apigatewayv2_integration.cors_integration.id}"
}

resource "aws_apigatewayv2_route" "rename_options" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "OPTIONS /rename-file"
  target    = "integrations/${aws_apigatewayv2_integration.cors_integration.id}"
}

resource "aws_apigatewayv2_route" "suggest_title_options" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "OPTIONS /suggest-title"
  target    = "integrations/${aws_apigatewayv2_integration.cors_integration.id}"
}

resource "aws_apigatewayv2_route" "summarize_options" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "OPTIONS /summarize"
  target    = "integrations/${aws_apigatewayv2_integration.cors_integration.id}"
} 