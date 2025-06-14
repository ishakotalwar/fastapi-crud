from fastapi import FastAPI, HTTPException
from models import Item

app = FastAPI()

db = []

@app.post("/items/")
def create_item(item: Item):
    db.append(item)
    return item

@app.get("/items/")
def read_items():
    return db

@app.get("/items/{item_id}")
def read_item(item_id: int):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(db):
        if item.id == item_id:
            db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(db):
        if item.id == item_id:
            del db[i]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
