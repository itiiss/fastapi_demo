from typing import Set, List, Union, Dict
from pydantic import BaseModel, Field, HttpUrl

from fastapi import FastAPI, Path, Query, Body

app = FastAPI()

# 路径参数校验, 和查询参数类似
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 第一个参数用*占位，后面的参数都是kwarg参数，不能缺省
@app.get("/kwargs/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

### 数值校验路径参数, item_id 大于等于1， q必穿
@app.get("/gtone/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

