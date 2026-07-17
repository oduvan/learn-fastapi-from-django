from django.test import TestCase


class FirstAppTests(TestCase):
    def test_root(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"message": "It works!"})

    def test_list_items(self):
        resp = self.client.get("/items")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            {
                "items": [
                    {"id": 1, "name": "Widget"},
                    {"id": 2, "name": "Gadget"},
                    {"id": 3, "name": "Gizmo"},
                ]
            },
        )

    def test_list_items_respects_limit(self):
        resp = self.client.get("/items?limit=1")
        self.assertEqual(resp.json(), {"items": [{"id": 1, "name": "Widget"}]})

    def test_get_item(self):
        resp = self.client.get("/items/2")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"id": 2, "name": "Gadget"})

    def test_get_item_missing_returns_404(self):
        resp = self.client.get("/items/999")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), {"detail": "Item not found"})

    def test_get_item_non_integer_returns_404(self):
        # Django's <int:...> converter simply doesn't match a non-int path,
        # so the URL resolver returns 404 (not a 422 like FastAPI).
        resp = self.client.get("/items/abc")
        self.assertEqual(resp.status_code, 404)
