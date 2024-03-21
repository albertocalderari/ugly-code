from pydantic import BaseModel

class Config:
    region = 'us-east-1'

class Order(BaseModel):
    id: str
    basket: list


class item(BaseModel):
    quantity: int
    name: str
    id: str
