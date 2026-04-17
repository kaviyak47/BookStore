import json
import os
import importlib.util
from decimal import Decimal
from unittest.mock import patch

os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"

def load_module():
    file_path = os.path.abspath("lambda/src/order-service/lambda_function.py")
    spec = importlib.util.spec_from_file_location("order_lambda_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


order_lambda = load_module()


@patch.object(order_lambda, "table")
def test_post_order_success(mock_table):
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "user_id": 1,
            "items": [
                {
                    "user_id": 1,
                    "product_id": 101,
                    "title": "Atomic Habits",
                    "price": 450,
                    "qty": 1
                }
            ],
            "total": 450
        })
    }

    response = order_lambda.lambda_handler(event, None)

    assert response["statusCode"] in [200, 201]
    body = json.loads(response["body"])
    assert "message" in body
    mock_table.put_item.assert_called_once()


@patch.object(order_lambda, "table")
def test_post_order_no_items(mock_table):
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "user_id": 1,
            "items": [],
            "total": 0
        })
    }

    response = order_lambda.lambda_handler(event, None)

    assert response["statusCode"] in [400, 422]
    body = json.loads(response["body"])
    assert "message" in body


@patch.object(order_lambda, "table")
def test_get_orders_success(mock_table):
    mock_table.scan.return_value = {
        "Items": [
            {
                "orderId": "abc123",
                "user_id": 1,
                "items": [{"title": "Atomic Habits", "qty": Decimal("1")}],
                "total": Decimal("450")
            }
        ]
    }

    event = {
        "httpMethod": "GET"
    }

    response = order_lambda.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert isinstance(body, list)
    assert body[0]["orderId"] == "abc123"