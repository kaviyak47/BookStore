import json
import boto3
import uuid
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")

orders_table = dynamodb.Table("Kaviya-orders")
cart_table = dynamodb.Table("Kaviya-Cart")


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=decimal_default)
    }


def get_body(event):
    try:
        return json.loads(event.get("body") or "{}")
    except Exception:
        return {}


def lambda_handler(event, context):
    try:
        method = event.get("httpMethod")

        if method == "OPTIONS":
            return response(200, {"message": "ok"})

        # PLACE ORDER
        elif method == "POST":
            body = get_body(event)

            user_id = str(body.get("user_id", "")).strip()
            items = body.get("items", [])
            total = body.get("total", 0)

            if not user_id:
                return response(400, {"message": "user_id required"})

            if not items or not isinstance(items, list):
                return response(400, {"message": "No selected items found"})

            order_items = []
            calculated_total = 0

            for item in items:
                product_id = int(item.get("product_id", 0))
                price = int(item.get("price", 0))
                qty = int(item.get("qty", 1))

                if product_id == 0:
                    return response(400, {"message": "product_id missing in one of the items"})

                order_item = {
                    "user_id": str(item.get("user_id", user_id)).strip(),
                    "product_id": product_id,
                    "title": item.get("title", ""),
                    "price": price,
                    "qty": qty
                }

                order_items.append(order_item)
                calculated_total += price * qty

            order = {
                "orderId": str(uuid.uuid4()),
                "user_id": user_id,
                "items": order_items,
                "total": int(calculated_total)
            }

            orders_table.put_item(Item=order)

            return response(200, {
                "message": "Order placed successfully",
                "order": order
            })

        # GET ORDERS BY USER
        elif method == "GET":
            query_params = event.get("queryStringParameters") or {}
            user_id = str(query_params.get("user_id", "")).strip()

            if not user_id:
                return response(400, {"message": "user_id required"})

            res = orders_table.scan(
                FilterExpression=Attr("user_id").eq(user_id)
            )

            return response(200, res.get("Items", []))

        return response(400, {"message": "Invalid request"})

    except Exception as e:
        return response(500, {"error": str(e)})