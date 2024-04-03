from pydantic import BaseModel


class Config:
    region = 'us-east-1'


class Order(BaseModel):
    id: str
    details: list


class GetOrder(BaseModel):
    id: str


class item(BaseModel):
    quantity: int
    name: str
    id: str


class User(BaseModel):
    id: str
    details: list


class GetUser(BaseModel):
    id: str


class UserDetails(BaseModel):
    name: str
    surname: str
