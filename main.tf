# -------------------------
# S3 Bucket (Frontend Hosting)
# -------------------------
resource "aws_s3_bucket" "frontend_bucket" {
  bucket = "kaviya-bookstore-frontend"
}

# -------------------------
# Public Access Block
# -------------------------
resource "aws_s3_bucket_public_access_block" "public" {
  bucket = aws_s3_bucket.frontend_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  restrict_public_buckets = false
  ignore_public_acls      = false
}

# -------------------------
# Bucket Policy (Public Read)
# -------------------------
resource "aws_s3_bucket_policy" "policy" {
  bucket = aws_s3_bucket.frontend_bucket.id

  depends_on = [
    aws_s3_bucket_public_access_block.public
  ]

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.frontend_bucket.arn}/*"
      }
    ]
  })
}

# -------------------------
# Upload Frontend Files
# -------------------------
resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = "index.html"
  source       = "frontend/index.html"
  content_type = "text/html"
}

resource "aws_s3_object" "products" {
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = "products.html"
  source       = "frontend/products.html"
  content_type = "text/html"
}

resource "aws_s3_object" "cart" {
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = "cart.html"
  source       = "frontend/cart.html"
  content_type = "text/html"
}

resource "aws_s3_object" "orders" {
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = "orders.html"
  source       = "frontend/orders.html"
  content_type = "text/html"
}

# -------------------------
# CloudFront CDN
# -------------------------
resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  default_root_object = "index.html"

  origin {
    domain_name = aws_s3_bucket.frontend_bucket.bucket_regional_domain_name
    origin_id   = "frontendS3"
  }

  default_cache_behavior {
    target_origin_id       = "frontendS3"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# =====================================================
# LAMBDA - PRODUCT SERVICE
# =====================================================
resource "aws_lambda_function" "product_service" {
  function_name = "Kaviya-Product-Service"
  role          = "arn:aws:iam::726101441380:role/service-role/Kaviya-Product-Service-role-t0s98gu5"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.14"

  filename         = "lambda/dist/product-service.zip"
  source_code_hash = filebase64sha256("lambda/dist/product-service.zip")

  timeout     = 3
  memory_size = 128
}

resource "aws_api_gateway_rest_api" "product_api" {
  name = "product-rest-api"
}

resource "aws_api_gateway_resource" "products" {
  rest_api_id = aws_api_gateway_rest_api.product_api.id
  parent_id   = aws_api_gateway_rest_api.product_api.root_resource_id
  path_part   = "products"
}

resource "aws_api_gateway_method" "products_get" {
  rest_api_id   = aws_api_gateway_rest_api.product_api.id
  resource_id   = aws_api_gateway_resource.products.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "products_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.product_api.id
  resource_id             = aws_api_gateway_resource.products.id
  http_method             = aws_api_gateway_method.products_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.product_service.invoke_arn
}

resource "aws_lambda_permission" "allow_api_gateway_product" {
  statement_id  = "AllowExecutionFromAPIGatewayProduct"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.product_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.product_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "product_deploy" {
  rest_api_id = aws_api_gateway_rest_api.product_api.id

  depends_on = [
    aws_api_gateway_integration.products_lambda
  ]
}

resource "aws_api_gateway_stage" "product_stage" {
  deployment_id = aws_api_gateway_deployment.product_deploy.id
  rest_api_id   = aws_api_gateway_rest_api.product_api.id
  stage_name    = "dev"
}

# =====================================================
# LAMBDA - CART SERVICE
# =====================================================
resource "aws_lambda_function" "cart_service" {
  function_name = "Kaviya-Cart-Service"
  role          = "arn:aws:iam::726101441380:role/service-role/Kaviya-Product-Service-role-t0s98gu5"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.14"

  filename         = "lambda/dist/cart-service.zip"
  source_code_hash = filebase64sha256("lambda/dist/cart-service.zip")

  timeout     = 3
  memory_size = 128
}

resource "aws_api_gateway_rest_api" "cart_api" {
  name = "cart-rest-api"
}

resource "aws_api_gateway_resource" "cart" {
  rest_api_id = aws_api_gateway_rest_api.cart_api.id
  parent_id   = aws_api_gateway_rest_api.cart_api.root_resource_id
  path_part   = "cart"
}

resource "aws_api_gateway_method" "cart_get" {
  rest_api_id   = aws_api_gateway_rest_api.cart_api.id
  resource_id   = aws_api_gateway_resource.cart.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "cart_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.cart_api.id
  resource_id             = aws_api_gateway_resource.cart.id
  http_method             = aws_api_gateway_method.cart_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cart_service.invoke_arn
}

resource "aws_lambda_permission" "allow_api_gateway_cart" {
  statement_id  = "AllowExecutionFromAPIGatewayCart"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cart_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.cart_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "cart_deploy" {
  rest_api_id = aws_api_gateway_rest_api.cart_api.id

  depends_on = [
    aws_api_gateway_integration.cart_lambda
  ]
}

resource "aws_api_gateway_stage" "cart_stage" {
  deployment_id = aws_api_gateway_deployment.cart_deploy.id
  rest_api_id   = aws_api_gateway_rest_api.cart_api.id
  stage_name    = "dev"
}

# =====================================================
# LAMBDA - ORDER SERVICE
# =====================================================
resource "aws_lambda_function" "order_service" {
  function_name = "Kaviya-Order-Service"
  role          = "arn:aws:iam::726101441380:role/service-role/Kaviya-Product-Service-role-t0s98gu5"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.14"

  filename         = "lambda/dist/order-service.zip"
  source_code_hash = filebase64sha256("lambda/dist/order-service.zip")

  timeout     = 3
  memory_size = 128
}

resource "aws_api_gateway_rest_api" "order_api" {
  name = "order-rest-api"
}

resource "aws_api_gateway_resource" "orders" {
  rest_api_id = aws_api_gateway_rest_api.order_api.id
  parent_id   = aws_api_gateway_rest_api.order_api.root_resource_id
  path_part   = "orders"
}

resource "aws_api_gateway_method" "orders_get" {
  rest_api_id   = aws_api_gateway_rest_api.order_api.id
  resource_id   = aws_api_gateway_resource.orders.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "orders_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.order_api.id
  resource_id             = aws_api_gateway_resource.orders.id
  http_method             = aws_api_gateway_method.orders_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.order_service.invoke_arn
}

resource "aws_lambda_permission" "allow_api_gateway_order" {
  statement_id  = "AllowExecutionFromAPIGatewayOrder"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.order_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.order_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "order_deploy" {
  rest_api_id = aws_api_gateway_rest_api.order_api.id

  depends_on = [
    aws_api_gateway_integration.orders_lambda
  ]
}

resource "aws_api_gateway_stage" "order_stage" {
  deployment_id = aws_api_gateway_deployment.order_deploy.id
  rest_api_id   = aws_api_gateway_rest_api.order_api.id
  stage_name    = "dev"
}
resource "aws_dynamodb_table" "cart_table" {
  name         = "Kaviya-Cart"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"
  range_key    = "product_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "product_id"
    type = "N"
  }

  tags = {
    Name        = "Kaviya-Cart"
    Environment = "dev"
    Project     = "BookStore"
  }
}
resource "aws_dynamodb_table" "users" {
  name         = "Kaviya-Users"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"

  attribute {
    name = "email"
    type = "S"
  }

  tags = {
    Name    = "Kaviya-Users"
    Project = "BookStore"
  }
}
resource "aws_iam_role" "auth_lambda_role" {
  name = "auth_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "auth_lambda_basic" {
  role       = aws_iam_role.auth_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "auth_lambda_dynamo" {
  role       = aws_iam_role.auth_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_lambda_function" "auth_lambda" {
  function_name = "Kaviya-Auth-Service"
  role          = aws_iam_role.auth_lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"

  filename         = "lambda/dist/auth.zip"
  source_code_hash = filebase64sha256("lambda/dist/auth.zip")
}
# =====================================================
# API GATEWAY - AUTH SERVICE
# =====================================================
resource "aws_api_gateway_rest_api" "auth_api" {
  name = "bookstore-auth-api"
}

resource "aws_api_gateway_resource" "signup_resource" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  parent_id   = aws_api_gateway_rest_api.auth_api.root_resource_id
  path_part   = "signup"
}

resource "aws_api_gateway_resource" "login_resource" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  parent_id   = aws_api_gateway_rest_api.auth_api.root_resource_id
  path_part   = "login"
}

# -------------------------
# SIGNUP POST
# -------------------------
resource "aws_api_gateway_method" "signup_post" {
  rest_api_id   = aws_api_gateway_rest_api.auth_api.id
  resource_id   = aws_api_gateway_resource.signup_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "signup_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.auth_api.id
  resource_id             = aws_api_gateway_resource.signup_resource.id
  http_method             = aws_api_gateway_method.signup_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.auth_lambda.invoke_arn
}

# -------------------------
# LOGIN POST
# -------------------------
resource "aws_api_gateway_method" "login_post" {
  rest_api_id   = aws_api_gateway_rest_api.auth_api.id
  resource_id   = aws_api_gateway_resource.login_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "login_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.auth_api.id
  resource_id             = aws_api_gateway_resource.login_resource.id
  http_method             = aws_api_gateway_method.login_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.auth_lambda.invoke_arn
}

# -------------------------
# SIGNUP OPTIONS
# -------------------------
resource "aws_api_gateway_method" "signup_options" {
  rest_api_id   = aws_api_gateway_rest_api.auth_api.id
  resource_id   = aws_api_gateway_resource.signup_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "signup_options_integration" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  resource_id = aws_api_gateway_resource.signup_resource.id
  http_method = aws_api_gateway_method.signup_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "signup_options_response" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  resource_id = aws_api_gateway_resource.signup_resource.id
  http_method = aws_api_gateway_method.signup_options.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "signup_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  resource_id = aws_api_gateway_resource.signup_resource.id
  http_method = aws_api_gateway_method.signup_options.http_method
  status_code = aws_api_gateway_method_response.signup_options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type'"
    "method.response.header.Access-Control-Allow-Methods" = "'POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_integration.signup_options_integration]
}

# -------------------------
# LOGIN OPTIONS
# -------------------------
resource "aws_api_gateway_method" "login_options" {
  rest_api_id   = aws_api_gateway_rest_api.auth_api.id
  resource_id   = aws_api_gateway_resource.login_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "login_options_integration" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  resource_id = aws_api_gateway_resource.login_resource.id
  http_method = aws_api_gateway_method.login_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "login_options_response" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  resource_id = aws_api_gateway_resource.login_resource.id
  http_method = aws_api_gateway_method.login_options.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "login_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  resource_id = aws_api_gateway_resource.login_resource.id
  http_method = aws_api_gateway_method.login_options.http_method
  status_code = aws_api_gateway_method_response.login_options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type'"
    "method.response.header.Access-Control-Allow-Methods" = "'POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_integration.login_options_integration]
}

# -------------------------
# API Gateway Permission
# -------------------------
resource "aws_lambda_permission" "allow_apigw_auth" {
  statement_id  = "AllowExecutionFromAPIGatewayAuth"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auth_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.auth_api.execution_arn}/*/*"
}

# -------------------------
# Deployment
# -------------------------
resource "aws_api_gateway_deployment" "auth_deploy" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id

  depends_on = [
    aws_api_gateway_integration.signup_post_integration,
    aws_api_gateway_integration.login_post_integration,
    aws_api_gateway_integration.signup_options_integration,
    aws_api_gateway_integration.login_options_integration
  ]
}

resource "aws_api_gateway_stage" "auth_stage" {
  deployment_id = aws_api_gateway_deployment.auth_deploy.id
  rest_api_id   = aws_api_gateway_rest_api.auth_api.id
  stage_name    = "dev"
}
resource "aws_s3_object" "signup" {
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = "signup.html"
  source       = "frontend/signup.html"
  content_type = "text/html"
}

resource "aws_s3_object" "login" {
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = "login.html"
  source       = "frontend/login.html"
  content_type = "text/html"
}
resource "aws_s3_object" "profile" {
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = "profile.html"
  source       = "frontend/profile.html"
  content_type = "text/html"
}