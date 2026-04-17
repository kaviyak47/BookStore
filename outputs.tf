output "product_api_url" {
  value = aws_api_gateway_stage.product_stage.invoke_url
}

output "cart_api_url" {
  value = aws_api_gateway_stage.cart_stage.invoke_url
}

output "order_api_url" {
  value = aws_api_gateway_stage.order_stage.invoke_url
}

output "frontend_url" {
  value = aws_cloudfront_distribution.cdn.domain_name
}