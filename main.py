# FastApi 处理Http入参数

 
from enum import Enum
from typing import List, Union
from fastapi import FastAPI, Query
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    
class Pet(str, Enum):
    DOG = "dog"
    CAT = "cat"
    HORSE = "horse"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


app = FastAPI()


# GET 入参
@app.get("/")
async def home():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/needy/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/pets/{pet}")
async def pet(pet: Pet):
    if pet is Pet.DOG:
        return {"pet": pet, "message": "Woof!"}

    if pet is Pet.CAT:
        return {"pet": pet, "message": "Meow!"}

    return {"pet": pet, "message": "Horse noises"}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# POST & PUT 入参
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    price_with_tax: float
    tax: Union[float, None] = None
    
@app.post("items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# 如果在路径中也声明了该参数，它将被用作路径参数。
# 如果参数属于单一类型（比如 int、float、str、bool 等）它将被解释为查询参数。
# 如果参数的类型被声明为一个 Pydantic 模型，它将被解释为请求体。
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# 参数校验
"""
通用的校验和元数据：alias, title, description, deprecated
特定于字符串的校验：min_length, max_length, regex
"""

# 将 Query 用作查询参数的默认值，并将它的 max_length 参数设置为 50
@app.get("/long/")
async def read_long(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get('/short')
# 参数q的最小长度需要10,且包含大小写和数字，参数默认值为'1234Ab'
async def read_short(q: Union[str, None] = Query('1234Ab', min_length=10, regex='^.*(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$')):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 入参 ‘qlist/?q=1&q=2’ 返回 {'q': ['1', '2']}
@app.get("/qlist/")
async def read_qlist(q: Union[List[str], None] = Query(default=['foo', 'bar'])):
    query_items = {"q": q}
    return query_items

# 使用 list 代替 List [str]，和上面等效
@app.get("/qlist2/")
async def read_qlist(q: list = Query(default=['foo', 'bar'])):
    query_items = {"q": q}
    return query_items

@app.get("/title/")
async def read_items(
    q: Union[str, None] = Query(default=None, title="Query string1", min_length=3)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results