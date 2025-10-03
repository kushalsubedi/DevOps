//113-171

resource "aws_lambda_function" "presign_lambda"{
    function_name="GeneratePresignURL"
    filename = "${path.module}/lambda/generate_upload_url.zip"
    role = aws_iam_role.lambda_exec_role.arn
    source_code_hash = filebase64sha256("${path.module}/lambda/generate_upload_url.zip")
    handler = "generate_upload_url.lambda_handler"
    runtime = "python3.12"
    environment {
        variables = {
            UPLOAD_BUCKET = aws_s3_bucket.upload_bucket.bucket
        }
    }
}

resource "aws_apigatewayv2_api" "upload_api" {
  name          = "SmartDriveAPI"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.upload_api.id
  integration_type = "AWS_PROXY"
  integration_method        = "POST"
  integration_uri           = aws_lambda_function.presign_lambda.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "get_presign_url" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "GET /generate-upload-url"

  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "options_presign_url" {
  api_id    = aws_apigatewayv2_api.upload_api.id
  route_key = "OPTIONS /generate-upload-url"

  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.upload_api.id
  name        = "$default"
  auto_deploy = true
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.presign_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.upload_api.execution_arn}/*/*"
}