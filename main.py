import logging

import boto3
from boto3.dynamodb.types import TypeDeserializer
from fastapi import FastAPI, Body
from starlette.responses import JSONResponse

from models import Config, GetOrder, Order

app = FastAPI()
from_dynamo = TypeDeserializer().deserialize
logger = logging.getLogger(__name__)

@app.get("/")
def health():
    return "Server is Healthy"


@app.get("/order/list", status_code=200)
def list_item() -> list:
    Client = boto3.client("dynamodb", Config.region)

    result = Client.scan(
        TableName='orders'
    )
    r = result['Items']
    logger.info(f"Fetched {len(r)} orders")
    return r


@app.post("/get-order", status_code=201)
def read_item(body: GetOrder = Body()):
    try:
        Client = boto3.client("dynamodb", Config.region)

        result = Client.get_item(
            TableName='orders',
            Key={
                'id': {
                    'S': body.id,
                }
            }
        )
        return Order.model_validate(from_dynamo(value={'M': result["Item"]}))
    except Exception as e:
        print(e)
        return JSONResponse(content="item not found", status_code=500)


@app.post("/get-order", status_code=201)
def read_item(body: GetOrder = Body()):
    Client = boto3.client("dynamodb", Config.region)

    result = Client.get_item(
        TableName='orders',
        Key={
            'id': {
                'S': body.id,
            }
        }
    )
    return Order.model_validate(from_dynamo(value={'M': result["Item"]}))
