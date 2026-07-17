from fastapi import FastAPI, HTTPException

app = FastAPI(title="First App (FastAPI)")

# In-memory data — the database comes in a later topic.
ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
    {"id": 3, "name": "Gizmo"},
]


@app.get("/")
def read_root():
    return {"message": "It works!"}


@app.get("/items")
def list_items(limit: int = 10):
    return {"items": ITEMS[:limit]}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
