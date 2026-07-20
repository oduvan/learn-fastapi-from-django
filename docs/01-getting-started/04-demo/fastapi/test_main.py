from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    assert client.get("/").json() == {"message": "It works!"}


def test_list_items():
    resp = client.get("/items")
    assert resp.status_code == 200
    assert resp.json() == {
        "items": [{"id": 1, "name": "Widget"}, {"id": 2, "name": "Gadget"}]
    }


def test_get_item():
    assert client.get("/items/1").json() == {"id": 1, "name": "Widget"}


def test_item_not_found():
    resp = client.get("/items/999")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Item not found"}


def test_list_users():
    resp = client.get("/users")
    assert resp.status_code == 200
    assert resp.json() == {
        "users": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Alan"}]
    }


def test_get_user():
    assert client.get("/users/2").json() == {"id": 2, "name": "Alan"}


def test_user_not_found():
    resp = client.get("/users/999")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User not found"}
