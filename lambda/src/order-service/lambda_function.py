import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Kaviya-orders")

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    method = event["httpMethod"]

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    try:
        if method == "POST":
            body = json.loads(event["body"])

            user_id = body.get("user_id")
            items = body.get("items", [])
            total = body.get("total", 0)

            if not items:
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"message": "No items selected"})
                }

            order = {
                "orderId": str(uuid.uuid4()),
                "user_id": user_id,
                "items": items,
                "total": total
            }

            table.put_item(Item=order)

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "Order placed successfully",
                    "order": order
                }, default=decimal_default)
            }

        elif method == "GET":
            response = table.scan()

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(response["Items"], default=decimal_default)
            }

        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": "Invalid request"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }