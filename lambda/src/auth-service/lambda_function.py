import json
import boto3
import base64
import hmac
import hashlib
import time
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Kaviya-Users")

JWT_SECRET = os.environ.get("JWT_SECRET", "kaviya-bookstore-secret-key")

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

def create_jwt(payload):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload["exp"] = int(time.time()) + 3600  # 1 hour expiry

    header_encoded = base64url_encode(json.dumps(header).encode())
    payload_encoded = base64url_encode(json.dumps(payload).encode())

    message = f"{header_encoded}.{payload_encoded}"

    signature = hmac.new(
        JWT_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()

    signature_encoded = base64url_encode(signature)

    return f"{message}.{signature_encoded}"

def lambda_handler(event, context):
    try:
        method = event.get("httpMethod")
        path = event.get("path")

        if method == "OPTIONS":
            return response(200, {"message": "ok"})

        body = json.loads(event.get("body") or "{}")

        if path.endswith("/signup"):
            email = body.get("email")
            name = body.get("name")
            password = body.get("password")
            role = body.get("role", "customer")

            if not email or not name or not password:
                return response(400, {"message": "Missing fields"})

            existing = table.get_item(Key={"email": email}).get("Item")

            if existing:
                return response(400, {"message": "User already exists"})

            table.put_item(Item={
                "email": email,
                "name": name,
                "password": password,
                "role": role
            })

            return response(200, {"message": "Signup successful"})

        if path.endswith("/login"):
            email = body.get("email")
            password = body.get("password")

            if not email or not password:
                return response(400, {"message": "Missing email or password"})

            user = table.get_item(Key={"email": email}).get("Item")

            if not user:
                return response(404, {"message": "User not found"})

            if user["password"] != password:
                return response(401, {"message": "Invalid password"})

            token = create_jwt({
                "email": user["email"],
                "name": user["name"],
                "role": user.get("role", "customer")
            })

            return response(200, {
                "message": "Login successful",
                "user": {
                    "email": user["email"],
                    "name": user["name"],
                    "role": user.get("role", "customer")
                },
                "token": token
            })

        return response(400, {"message": "Invalid request"})

    except Exception as e:
        return response(500, {"message": str(e)})