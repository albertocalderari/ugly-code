import logging

import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from fastapi import FastAPI, Body, APIRouter
from starlette.responses import JSONResponse, PlainTextResponse

from models import Config, GetOrder, Order
from router import user_router

app = FastAPI()
app.include_router(user_router)
from_dynamo = TypeDeserializer().deserialize
logger = logging.getLogger(__name__)
to_dynamo = TypeSerializer().serialize


@app.get("/")
def health():
    return "Server is Healthy"


order_router = APIRouter(tags=['order'])


@order_router.get("/order/list", status_code=200)
def list_item() -> list:
    Client = boto3.client("dynamodb", Config.region)

    result = Client.scan(
        TableName='orders'
    )
    its: None | list = result.get('Items')
    try:
        match its:
            case []:
                raise ValueError("no results")
        r = result['Items']
        print(r)
    except Exception:
        return PlainTextResponse(content="not found", status_code=404)
    logger.info(f"Fetched {len(result['Items'])} orders")
    return result['Items']


@order_router.post("/get-order", status_code=201)
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


@order_router.post("/get-order", status_code=201)
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


@order_router.post("/create-order")
def read_item(body: Order = Body()):
    try:
        Client = boto3.client("dynamodb", Config.region)
        dynamo_details = to_dynamo(body.details)
        hash_key = to_dynamo(body.id)
        Client.put_item(
            TableName='orders',
            Item={
                "id": hash_key,
                "details": dynamo_details
            }
        )
        content = {
            "message": "item added"
        }
        return JSONResponse(content=content, status_code=200)
    except Exception:
        return JSONResponse(content="could not write item", status_code=200)


@order_router.post("/update-order")
def read_item(body: Order = Body()):
    try:
        Client = boto3.client("dynamodb", Config.region)

        hash_key = to_dynamo(body.id)
        r = Client.get_item(
            TableName='orders',
            Key={
                'id': hash_key
            }
        )
        try:
            _ = r['Item']
        except KeyError:
            raise ValueError("Error")

        Client = boto3.client("dynamodb", Config.region)
        dynamo_details = to_dynamo(body.details)
        Client.put_item(
            TableName='orders',
            Item={
                "id": hash_key,
                "details": dynamo_details
            }
        )
        content = {
            "message": "item added"
        }
        return JSONResponse(content=content, status_code=200)
    except Exception:
        return JSONResponse(content="could not write item", status_code=200)


app.include_router(order_router)
