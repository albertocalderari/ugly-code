import boto3
from fastapi import FastAPI

from models import Config

app = FastAPI()


@app.get("/")
def health():
    return "Server is Healthy"


@app.get("/order/list")
def read_item() -> list:
    Client = boto3.client("dynamodb", Config.region)

    result = Client.scan(
        Table='order'
    )
    r = result['Items']
    return r
