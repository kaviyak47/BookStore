import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Kaviya-Users")

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

def lambda_handler(event, context):
    try:
        method = event.get("httpMethod")
        path = event.get("path")

        if method == "OPTIONS":
            return response(200, {"message": "ok"})

        body = json.loads(event.get("body") or "{}")

        # SIGNUP
        if path.endswith("/signup"):
            email = body.get("email")
            name = body.get("name")
            password = body.get("password")
            role = body.get("role", "customer")

            if not email or not password:
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

        # LOGIN
        if path.endswith("/login"):
            email = body.get("email")
            password = body.get("password")

            user = table.get_item(Key={"email": email}).get("Item")

            if not user:
                return response(404, {"message": "User not found"})

            if user["password"] != password:
                return response(401, {"message": "Invalid password"})

            return response(200, {
                "message": "Login successful",
                "user": {
                    "email": user["email"],
                    "name": user["name"],
                    "role": user["role"]
                }
            })

        return response(400, {"message": "Invalid request"})

    except Exception as e:
        return response(500, {"message": str(e)})