import json
import os
import importlib.util
from decimal import Decimal
from unittest.mock import patch

os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"

def load_module():
    file_path = os.path.abspath("lambda/src/product-service/lambda_function.py")
    spec = importlib.util.spec_from_file_location("product_lambda_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


product_lambda = load_module()


@patch.object(product_lambda, "table")
def test_get_products(mock_table):
    mock_table.scan.return_value = {
        "Items": [
            {
                "id": 1,
                "title": "Atomic Habits",
                "price": Decimal("450")
            },
            {
                "id": 2,
                "title": "Clean Code",
                "price": Decimal("500")
            }
        ]
    }

    event = {
        "httpMethod": "GET"
    }

    response = product_lambda.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert isinstance(body, list)
    assert len(body) == 2
    assert body[0]["title"] == "Atomic Habits"


def test_invalid_method():
    event = {
        "httpMethod": "PUT"
    }

    response = product_lambda.lambda_handler(event, None)

    assert response["statusCode"] in [400, 405]