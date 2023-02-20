# 请求体多参数校验
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    price_with_tax: float
    tax: Union[float, None] = None
    
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    
@app.put("/item/{item_id}")
# 更新item，其中item_id 需要是大于10的整数，item可能为None
async def update_item(*, item_id: int = Path(ge=10), item: Union[Item, None] = None):
    results = {"item_id": item_id}
    if item:
        results.update({"item": item})
    return results

@app.put("/user/{user_id}/item/{item_id}")
# 更新item和user
async def update_item(
    *,
    user_id: int = Path(ge=10),
    item_id: int = Path(ge=10),
    item: Union[Item, None] = None,
    user: Union[User, None] = None,
):
    results = {"item_id": item_id, "user_id": user_id}
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    return results

"""
此时需要这样的一个请求体，item, user和importance组成一个JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
"""
@app.put("/body/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

"""
此时需要这样的一个请求体，多了一级item
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
"""
@app.put("/embed/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

# 校验请求体字段，把和Path，Query，Body类似的Field作用到 Model的字段里
class ValidItem(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None
    
@app.put("/valid_item/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

# 将某个字段设置成list

class Image(BaseModel):
    url: HttpUrl # 除了int，str，float之外，还有很多类型，比如HttpUrl，EmailStr，UUID4，等等更精确的类型
    name: str

class ItemWithList(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = [] # Set[str] = set() 使用set也可以
    image: Union[Image, None] = None # 模型之前也可以自由组合，也不限层次
    
@app.put("/list_items/{item_id}")
async def update_item(item_id: int, item: ItemWithList):
    results = {"item_id": item_id, "item": item}
    return results

# 请求体直接是个列表
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images
# 请求体是个Dict，但是预先知道 dict的key是int类型，value是float类型
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
