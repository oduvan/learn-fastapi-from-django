from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "It works!"}


def test_list_items():
    resp = client.get("/items")
    assert resp.status_code == 200
    assert resp.json() == {
        "items": [
            {"id": 1, "name": "Widget"},
            {"id": 2, "name": "Gadget"},
            {"id": 3, "name": "Gizmo"},
        ]
    }


def test_list_items_respects_limit():
    resp = client.get("/items?limit=1")
    assert resp.json() == {"items": [{"id": 1, "name": "Widget"}]}


def test_get_item():
    resp = client.get("/items/2")
    assert resp.status_code == 200
    assert resp.json() == {"id": 2, "name": "Gadget"}


def test_get_item_missing_returns_404():
    resp = client.get("/items/999")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Item not found"}


def test_get_item_non_integer_returns_422():
    # FastAPI validates the path type: a non-int id is a 422, not a 404.
    resp = client.get("/items/abc")
    assert resp.status_code == 422
