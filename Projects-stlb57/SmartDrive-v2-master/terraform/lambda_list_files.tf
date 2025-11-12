//List Files Lambda
resource "aws_lambda_function" "list_files_lambda" {
  function_name    = "ListOrganizedFiles"
  filename         = "${path.module}/lambda/list_files.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/list_files.zip")
  handler          = "list_files.lambda_handler"
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_exec_role.arn

  environment {
    variables = {
      ORGANIZED_BUCKET = aws_s3_bucket.organized_bucket.bucket
    }
  }
}

resource "aws_apigatewayv2_integration" "list_files_integration" {
  api_id                 = aws_apigatewayv2_api.upload_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.list_files_lambda.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "list_files_route" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "GET /list-files"
  target    = "integrations/${aws_apigatewayv2_integration.list_files_integration.id}"
}

resource "aws_lambda_permission" "list_files_permission" {
  statement_id  = "AllowListFilesFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.list_files_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}

output "upload_api_url" {
  description = "API Gateway endpoint for generating pre-signed S3 upload URLs"
  value       = aws_apigatewayv2_api.upload_api.api_endpoint
}

