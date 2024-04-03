import logging

import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from fastapi import Body
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse, PlainTextResponse

from models import Config, GetUser, User

user_router = APIRouter(tags=['user'])
from_dynamo = TypeDeserializer().deserialize
logger = logging.getLogger(__name__)
to_dynamo = TypeSerializer().serialize

@user_router.get("/user/list", status_code=200)
def list_item() -> list:
    Client = boto3.client("dynamodb", Config.region)

    result = Client.scan(
        TableName='users'
    )
    items: None | list = result.get('Items')
    try:
        match items:
            case list():
                raise ValueError("no results")
        r = result['Items']
        print(r)
    except Exception:
        return PlainTextResponse(content="not found", status_code=404)
    logger.info(f"Fetched {len(result['Items'])} users")
    return result['Items']


@user_router.post("/get-user", status_code=201)
def read_item(body: GetUser = Body()):
    try:
        Client = boto3.client("dynamodb", Config.region)

        result = Client.get_item(
            TableName='users',
            Key={
                'id': {
                    'S': body.id,
                }
            }
        )
        return User.model_validate(from_dynamo(value={'M': result["Item"]}))
    except Exception as e:
        print(e)
        return JSONResponse(content="item not found", status_code=500)


@user_router.post("/get-user", status_code=201)
def read_item(body: GetUser = Body()):
    Client = boto3.client("dynamodb", Config.region)

    result = Client.get_item(
        TableName='users',
        Key={
            'id': {
                'S': body.id,
            }
        }
    )
    return User.model_validate(from_dynamo(value={'M': result["Item"]}))


@user_router.post("/create-user")
def read_item(body: User = Body()):
    try:
        Client = boto3.client("dynamodb", Config.region)
        dynamo_details = to_dynamo(body.details)
        hash_key = to_dynamo(body.id)
        Client.put_item(
            TableName='users',
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


@user_router.post("/update-user")
def read_item(body: User = Body()):
    try:
        Client = boto3.client("dynamodb", Config.region)

        hash_key = to_dynamo(body.id)
        r = Client.get_item(
            TableName='users',
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
            TableName='users',
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
