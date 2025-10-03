
resource "aws_lambda_function" "suggest_title_lambda" {
  function_name    = "SuggestTitleLambda"
  filename         = "${path.module}/lambda/suggest_title.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/suggest_title.zip")
  handler          = "suggest_title.lambda_handler"
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_exec_role.arn

  # FIX: Add timeout and memory settings
  timeout     = 60 # 60 seconds
  memory_size = 256 # 256 MB (more than enough for this lightweight version)

  environment {
    variables = {
      # FIX: Correct variable name and add the API token
      ORGANIZED_BUCKET = aws_s3_bucket.organized_bucket.bucket
      HF_API_TOKEN = var.huggingface_api_token # Replace with your actual token
    }
  }
}

resource "aws_apigatewayv2_integration" "suggest_title_integration" {
  api_id                 = aws_apigatewayv2_api.upload_api.id
  integration_type       = "AWS_PROXY"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.suggest_title_lambda.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post_suggest_title" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "POST /suggest-title"
  target    = "integrations/${aws_apigatewayv2_integration.suggest_title_integration.id}"
}

resource "aws_lambda_permission" "api_permission_suggest_title" {
  statement_id  = "AllowAPIGatewayInvokeSuggestTitle"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.suggest_title_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}