import json
import boto3
from decimal import Decimal

# DynamoDB connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Kaviya-Products')

# Convert Decimal → JSON safe
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

# CORS headers (IMPORTANT)
def get_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

def lambda_handler(event, context):

    try:
        method = event.get("httpMethod")
        path_params = event.get("pathParameters") or {}
        body = {}

        if event.get("body"):
            try:
                body = json.loads(event["body"])
            except:
                body = {}

        # -------------------------
        # OPTIONS (CORS preflight)
        # -------------------------
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": get_headers(),
                "body": ""
            }

        # -------------------------
        # GET /products or /products/{id}
        # -------------------------
        if method == "GET":

            book_id = path_params.get("id")

            if book_id:
                book_id = int(book_id)

                response = table.get_item(Key={"id": book_id})

                if "Item" in response:
                    return {
                        "statusCode": 200,
                        "headers": get_headers(),
                        "body": json.dumps(response["Item"], default=decimal_default)
                    }

                return {
                    "statusCode": 404,
                    "headers": get_headers(),
                    "body": json.dumps({"message": "Product not found"})
                }

            else:
                response = table.scan()

                return {
                    "statusCode": 200,
                    "headers": get_headers(),
                    "body": json.dumps(response.get("Items", []), default=decimal_default)
                }

        # -------------------------
        # POST /products
        # -------------------------
        if method == "POST":

            product = body.get("product")

            if not product:
                return {
                    "statusCode": 400,
                    "headers": get_headers(),
                    "body": json.dumps({"message": "Product data required"})
                }

            table.put_item(Item=product)

            return {
                "statusCode": 201,
                "headers": get_headers(),
                "body": json.dumps({
                    "message": "Product added successfully",
                    "product": product
                })
            }

        # -------------------------
        # Invalid method
        # -------------------------
        return {
            "statusCode": 400,
            "headers": get_headers(),
            "body": json.dumps({"message": "Invalid method"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": get_headers(),
            "body": json.dumps({"error": str(e)})
        }