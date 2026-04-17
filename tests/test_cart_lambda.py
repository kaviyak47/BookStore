import json
import os
import importlib.util
from decimal import Decimal
from unittest.mock import patch


os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"
def load_module():
    file_path = os.path.abspath("lambda/src/cart-service/lambda_function.py")
    spec = importlib.util.spec_from_file_location("cart_lambda_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cart_lambda = load_module()


@patch.object(cart_lambda, "table")
def test_get_cart_success(mock_table):
    mock_table.scan.return_value = {
        "Items": [
            {
                "user_id": 1,
                "product_id": 101,
                "title": "Atomic Habits",
                "price": Decimal("450"),
                "qty": Decimal("1"),
            }
        ]
    }

    event = {
        "httpMethod": "GET",
        "queryStringParameters": {"user_id": "1"},
    }

    response = cart_lambda.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert isinstance(body, list)
    assert body[0]["title"] == "Atomic Habits"
    assert body[0]["product_id"] == 101


@patch.object(cart_lambda, "table")
def test_post_cart_add_new_item(mock_table):
    mock_table.get_item.return_value = {}

    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "user_id": 1,
            "product_id": 101,
            "title": "Atomic Habits",
            "price": 450,
            "qty": 1
        })
    }

    response = cart_lambda.lambda_handler(event, None)

    assert response["statusCode"] in [200, 201]
    body = json.loads(response["body"])
    assert "message" in body
    mock_table.put_item.assert_called_once()


@patch.object(cart_lambda, "table")
def test_post_cart_update_existing_item(mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "user_id": 1,
            "product_id": 101,
            "qty": 2
        }
    }

    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "user_id": 1,
            "product_id": 101,
            "title": "Atomic Habits",
            "price": 450,
            "qty": 1
        })
    }

    response = cart_lambda.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "message" in body
    mock_table.update_item.assert_called_once()


@patch.object(cart_lambda, "table")
def test_put_cart_quantity_update(mock_table):
    event = {
        "httpMethod": "PUT",
        "body": json.dumps({
            "user_id": 1,
            "product_id": 101,
            "qty": 3
        })
    }

    response = cart_lambda.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "message" in body
    mock_table.update_item.assert_called_once()


@patch.object(cart_lambda, "table")
def test_delete_cart_item(mock_table):
    event = {
        "httpMethod": "DELETE",
        "body": json.dumps({
            "user_id": 1,
            "product_id": 101
        })
    }

    response = cart_lambda.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "message" in body
    mock_table.delete_item.assert_called_once()