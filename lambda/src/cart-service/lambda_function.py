import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Kaviya-Cart")


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError(f"Type not serializable: {type(obj)}")


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=decimal_default)
    }


def get_method(event):
    return event.get("httpMethod", "")


def get_body(event):
    try:
        return json.loads(event.get("body") or "{}")
    except Exception:
        return {}


def lambda_handler(event, context):
    try:
        method = get_method(event)

        # CORS preflight
        if method == "OPTIONS":
            return response(200, {"message": "ok"})

        # GET /cart?user_id=1
        elif method == "GET":
            query_params = event.get("queryStringParameters") or {}
            user_id = int(query_params.get("user_id", 1))

            res = table.scan(
                FilterExpression=Attr("user_id").eq(user_id)
            )

            return response(200, res.get("Items", []))

        # POST /cart
        # add item if new, otherwise increase qty
        elif method == "POST":
            body = get_body(event)

            user_id = int(body.get("user_id", 1))
            product_id = int(body.get("product_id", 0))
            title = body.get("title", "")
            price = int(body.get("price", 0))
            qty = int(body.get("qty", 1))

            if product_id == 0:
                return response(400, {"error": "product_id required"})

            existing = table.get_item(
                Key={
                    "user_id": user_id,
                    "product_id": product_id
                }
            ).get("Item")

            if existing:
                new_qty = int(existing.get("qty", 1)) + qty

                table.update_item(
                    Key={
                        "user_id": user_id,
                        "product_id": product_id
                    },
                    UpdateExpression="SET qty = :q, title = :t, price = :p",
                    ExpressionAttributeValues={
                        ":q": new_qty,
                        ":t": title,
                        ":p": price
                    }
                )

                return response(200, {
                    "message": "Cart updated",
                    "user_id": user_id,
                    "product_id": product_id,
                    "qty": new_qty
                })

            table.put_item(
                Item={
                    "user_id": user_id,
                    "product_id": product_id,
                    "title": title,
                    "price": price,
                    "qty": qty
                }
            )

            return response(200, {
                "message": "Added successfully",
                "user_id": user_id,
                "product_id": product_id,
                "qty": qty
            })

        # PUT /cart
        # set qty directly
        elif method == "PUT":
            body = get_body(event)

            user_id = int(body.get("user_id", 0))
            product_id = int(body.get("product_id", 0))
            qty = int(body.get("qty", 0))

            if user_id == 0 or product_id == 0:
                return response(400, {"error": "user_id and product_id required"})

            if qty <= 0:
                table.delete_item(
                    Key={
                        "user_id": user_id,
                        "product_id": product_id
                    }
                )

                return response(200, {"message": "Item removed"})

            table.update_item(
                Key={
                    "user_id": user_id,
                    "product_id": product_id
                },
                UpdateExpression="SET qty = :q",
                ExpressionAttributeValues={
                    ":q": qty
                }
            )

            return response(200, {
                "message": "Quantity updated",
                "user_id": user_id,
                "product_id": product_id,
                "qty": qty
            })

        # DELETE /cart
        elif method == "DELETE":
            body = get_body(event)

            user_id = int(body.get("user_id", 0))
            product_id = int(body.get("product_id", 0))

            if user_id == 0 or product_id == 0:
                return response(400, {"error": "user_id and product_id required"})

            table.delete_item(
                Key={
                    "user_id": user_id,
                    "product_id": product_id
                }
            )

            return response(200, {
                "message": "Item deleted",
                "user_id": user_id,
                "product_id": product_id
            })

        return response(400, {"message": "Invalid method"})

    except Exception as e:
        return response(500, {"error": str(e)})