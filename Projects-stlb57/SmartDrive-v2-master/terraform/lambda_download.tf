resource "aws_lambda_function" "get_download_url" {
  function_name = "GetDownloadURL"
  filename      = "${path.module}/lambda/get_download_url.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/get_download_url.zip")
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "get_download_url.lambda_handler"
  runtime       = "python3.12"

  environment {
    variables = {
      ORGANIZED_BUCKET = aws_s3_bucket.organized_bucket.bucket
    }
  }
}

resource "aws_apigatewayv2_integration" "download_integration" {
  api_id           = aws_apigatewayv2_api.upload_api.id
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  integration_uri  = aws_lambda_function.get_download_url.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "download_route" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "GET /get-download-url"
  target    = "integrations/${aws_apigatewayv2_integration.download_integration.id}"
}

resource "aws_apigatewayv2_route" "download_options" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "OPTIONS /get-download-url"
  target    = "integrations/${aws_apigatewayv2_integration.download_integration.id}"
}

resource "aws_lambda_permission" "allow_get_download_url" {
  statement_id  = "AllowDownloadURL"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_download_url.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}
