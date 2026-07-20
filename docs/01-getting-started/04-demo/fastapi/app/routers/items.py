from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/items", tags=["items"])

ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
]


@router.get("")
def list_items():
    return {"items": ITEMS}


@router.get("/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
