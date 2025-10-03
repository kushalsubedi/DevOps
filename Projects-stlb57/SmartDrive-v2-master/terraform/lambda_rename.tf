resource "aws_lambda_function" "rename_file" {
  function_name = "RenameFile"
  filename      = "${path.module}/lambda/rename_file.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/rename_file.zip")
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "rename_file.lambda_handler"
  runtime       = "python3.12"

  environment {
    variables = {
      ORGANIZED_BUCKET = aws_s3_bucket.organized_bucket.bucket
    }
  }
}

resource "aws_apigatewayv2_integration" "rename_integration" {
  api_id           = aws_apigatewayv2_api.upload_api.id
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  integration_uri  = aws_lambda_function.rename_file.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "rename_route" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "POST /rename-file"
  target    = "integrations/${aws_apigatewayv2_integration.rename_integration.id}"
}



resource "aws_lambda_permission" "allow_rename_file" {
  statement_id  = "AllowRenameFile"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rename_file.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}
