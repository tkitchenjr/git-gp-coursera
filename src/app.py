from database import get_db, startup_event
from fastapi import FastAPI
from models import Item
app = FastAPI()
app.add_event_handler("startup", startup_event)
@app.post("/items/")
def create_item(item:Item):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, price, is_offer) VALUES (?, ?, ?)", (item.name, item.price, int(item.is_offer) if item.is_offer else None), )
    conn.commit()
    item.id = cursor.lastrowid
    return item

## Update items API route ##

@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    conn = get_db()
    conn.execute(
        "UPDATE items SET name = ?, price = ?, is_offer = ? WHERE id = ?",
        (item.name, item.price, int(item.is_offer) 
        if item.is_offer 
        else None, item_id),)
    conn.commit()
    return item

## Delete items API route ##

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    return {"message": "Item deleted"}

## Read items API route ##

@app.get("/items/")
def read_items():
    conn = get_db()
    items = conn.execute("SELECT * FROM items").fetchall()
    return [
        dict(item) for item in items]

## Read item API route ##

@app.get("/items/{item_id}")
def read_item(item_id:int):
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if item is None:
        raise HTTPException(
            status_code=404, 
    detail="Item not found"
            )
    return dict(item)
