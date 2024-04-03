from typing import Any, Iterable

import boto3
from moto import mock_aws
from pytest import fixture
from starlette.testclient import TestClient
from boto3.dynamodb.types import TypeSerializer

from models import item

to_dynamo = TypeSerializer().serialize


@fixture
def items() -> list[item]:
    return [
        item(
            quantity=2,
            name="chicken",
            id="1",
        ),
        item(
            quantity=1,
            name="pork",
            id="2",
        ),
        item(
            quantity=1,
            name="fries",
            id="3",
        ),
        item(
            quantity=50,
            name="beer",
            id="4",
        ),
    ]


@fixture()
def orders(items) -> Iterable[tuple[str, list[dict[str, Any]]]]:
    out = []
    for idx in range(0, 200):
        basket_size = idx % 3 + 1
        basket = [i.model_dump() for i in items[:basket_size]]
        order = (f"{idx}", basket)
        out.append(order)
    return out


@fixture()
def setup_dynamo(orders, monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    with mock_aws():
        c = boto3.client("dynamodb")
        c.create_table(
            TableName='orders',
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        for order_id, basket in orders:
            dynamo_basket = to_dynamo(basket)
            hash_key = to_dynamo(order_id)
            c.put_item(
                TableName='orders',
                Item={
                    "id": hash_key,
                    "basket": dynamo_basket
                }
            )
        yield c


@fixture
def client(setup_dynamo):
    with mock_aws():
        from main import app
        yield TestClient(app)
