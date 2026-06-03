import json
import boto3
from decimal import Decimal
import base64
import hmac
import hashlib
import time
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Kaviya-Products")

JWT_SECRET = os.environ.get("JWT_SECRET", "kaviya-bookstore-secret-key")

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def get_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Content-Type": "application/json"
    }

def make_response(status, body):
    return {
        "statusCode": status,
        "headers": get_headers(),
        "body": json.dumps(body, default=decimal_default)
    }

def base64url_decode(data):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def verify_jwt(token):
    try:
        parts = token.split(".")

        if len(parts) != 3:
            return None

        header_encoded, payload_encoded, signature_encoded = parts
        message = f"{header_encoded}.{payload_encoded}"

        expected_signature = hmac.new(
            JWT_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()

        actual_signature = base64url_decode(signature_encoded)

        if not hmac.compare_digest(expected_signature, actual_signature):
            return None

        payload = json.loads(base64url_decode(payload_encoded))

        if payload.get("exp") and int(time.time()) > payload["exp"]:
            return None

        return payload

    except Exception:
        return None

def get_logged_user(event):
    headers = event.get("headers") or {}
    auth_header = headers.get("Authorization") or headers.get("authorization")

    if not auth_header:
        return None

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "").strip()
    return verify_jwt(token)

def lambda_handler(event, context):
    try:
        method = event.get("httpMethod")
        path_params = event.get("pathParameters") or {}

        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": get_headers(),
                "body": ""
            }

        body = {}

        if event.get("body"):
            try:
                body = json.loads(event["body"])
            except:
                body = {}

        if method == "GET":
            book_id = path_params.get("id")

            if book_id:
                book_id = int(book_id)
                result = table.get_item(Key={"id": book_id})

                if "Item" in result:
                    return make_response(200, result["Item"])

                return make_response(404, {"message": "Product not found"})

            result = table.scan()
            return make_response(200, result.get("Items", []))

        if method == "POST":
            logged_user = get_logged_user(event)

            if not logged_user:
                return make_response(401, {"message": "Unauthorized. Token missing or invalid."})

            if logged_user.get("role") != "admin":
                return make_response(403, {"message": "Only admin can add products"})

            product = body.get("product")

            if not product:
                return make_response(400, {"message": "Product data required"})

            required_fields = ["id", "title", "price", "author", "image"]

            for field in required_fields:
                if field not in product or product[field] in ["", None]:
                    return make_response(400, {"message": f"{field} is required"})

            product["id"] = int(product["id"])
            product["price"] = int(product["price"])

            table.put_item(Item=product)

            return make_response(201, {
                "message": "Product added successfully",
                "product": product
            })

        return make_response(400, {"message": "Invalid method"})

    except Exception as e:
        return make_response(500, {"error": str(e)})