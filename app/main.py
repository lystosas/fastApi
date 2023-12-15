import os
from typing import List, Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

# templates = Jinja2Templates(directory="templates")


# Models
class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool


class User(BaseModel):
    id: int
    name: str
    email: str


class Order(BaseModel):
    id: int
    user_id: int
    products: List[Product]
    total_price: float


# Data

products = [
    Product(id=1, name="Dolex Jarabe", price=14500, in_stock=True),
    Product(id=2, name="Acetaminofen Jarabe", price=4500, in_stock=True),
]

user = [
    User(id=1, name="Giovanni", email="davison2494@gmail.com"),
]

orders = []


@app.get("/api")
async def read_root():
    return {"Hello": "Davis Giovanni Chamorro"}


@app.get("/favicon.ico")
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "app/static", file_name)
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": "attachment; filename=" + file_name},
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Rutas
@app.get("/products", tags=["Products"])
def getProducts():
    return products


@app.post("products", tags=["Products"])
def addProduct(product: Product):
    # se verifica si el producto existe
    for p in product:
        if p.id == product.id:
            raise HTTPException(status_code=400, detail="El Producto ya existe")

    products.append(product)
    return product


@app.put("/products/{product_id}", tags=["Products"])
def updateProduct(product_id: int, product: Product):
    for idx, p in enumerate(products):
        if p.id == product_id:
            products[idx] = product
            return product
    return {"error": "Producto no encontrado"}


@app.delete("/products/{product_id}", tags=["Products"])
def deleteProduct(product_id: int):
    for idx, p in enumerate(products):
        if p.id == product_id:
            del products[idx]
            return {"message": "Producto eliminado"}
    return {"error": "Producto no encontrado"}


@app.post("/users", tags=["Users"])
def createUser(user: User):
    user.append(user)
    return user


@app.put("/users/{user_id}", tags=["Users"])
def updateUser(user_id: int, user: User):
    for idx, u in enumerate(user):
        if u.id == user_id:
            user[idx] = user
            return user
    return {"error": "Usuario no encontrado"}


@app.delete("/users/{user_id}", tags=["Users"])
def deleteUser(user_id: int):
    for idx, u in enumerate(user_id):
        if u.id == user_id:
            del user_id[idx]
            return {"message": "Usuario eliminado"}
    return {"error": "Usuario no encontrado"}


# Tarea
@app.get("/orders", tags=["Orders"])
def get_orders():
    # TAREA
    return orders


@app.post("/orders", tags=["Orders"])
def create_order(order: Order):
    # TAREA

    newOrder = Order(
        id=order.id,
        user_id=order.user_id,
        products=order.products,
        total_price=sum(p.price for p in order.products),
    )
    orders.append(newOrder)
    return {"message": "Orden creada"}


@app.put("/orders", tags=["Orders"])
def update_order():
    # TAREA
    return {"message": "Orden actualizada"}


@app.delete("/orders", tags=["Orders"])
def delete_order():
    # TAREA
    return {"message": "Orden eliminada"}
