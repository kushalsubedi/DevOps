resource "aws_lambda_function" "stats" {
  function_name = "StatsFunction"
  filename      = "${path.module}/lambda/stats.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/stats.zip")
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "stats.lambda_handler"
  runtime       = "python3.12"

  environment {
    variables = {
      ORGANIZED_BUCKET = aws_s3_bucket.organized_bucket.bucket
    }
  }
}

resource "aws_apigatewayv2_integration" "stats_integration" {
  api_id           = aws_apigatewayv2_api.upload_api.id
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  integration_uri  = aws_lambda_function.stats.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "stats_route" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "GET /stats"
  target    = "integrations/${aws_apigatewayv2_integration.stats_integration.id}"
}

resource "aws_lambda_permission" "allow_stats" {
  statement_id  = "AllowStats"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.stats.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}
