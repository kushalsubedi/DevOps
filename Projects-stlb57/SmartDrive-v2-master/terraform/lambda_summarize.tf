variable "huggingface_api_token" {
  type      = string
  sensitive = true
}

resource "aws_lambda_function" "summarize_lambda" {
  function_name = "SummarizeLambda"
  filename         = "${path.module}/lambda/summarize.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/summarize.zip")
  handler          = "summarize.lambda_handler"
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_exec_role.arn

  timeout     = 120  # 120 seconds (2 minutes) provides a safe buffer
  memory_size = 256  # 256 MB is sufficient for this lightweight function

  environment {
    variables = {
      BUCKET = "${aws_s3_bucket.organized_bucket.bucket}"
      HF_API_TOKEN = var.huggingface_api_token
    }
  }
}

resource "aws_apigatewayv2_integration" "summarize_integration" {
  api_id                 = aws_apigatewayv2_api.upload_api.id
  integration_type       = "AWS_PROXY"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.summarize_lambda.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post_summarize" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "POST /summarize"
  target    = "integrations/${aws_apigatewayv2_integration.summarize_integration.id}"
}

resource "aws_lambda_permission" "api_permission_summarize" {
  statement_id  = "AllowAPIGatewayInvokeSummarize"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.summarize_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}


