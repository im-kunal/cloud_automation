from typing import Union, Any
from fastapi import FastAPI, Request
from service_set import service_set

app = FastAPI()


@app.get("/")
def welcome():
    return {"Message": "Welcome to my Cloud Automation Project"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
