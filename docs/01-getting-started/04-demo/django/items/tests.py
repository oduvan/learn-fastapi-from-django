from django.test import TestCase


class ItemTests(TestCase):
    def test_list_items(self):
        resp = self.client.get("/items")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            {"items": [{"id": 1, "name": "Widget"}, {"id": 2, "name": "Gadget"}]},
        )

    def test_get_item(self):
        self.assertEqual(
            self.client.get("/items/1").json(), {"id": 1, "name": "Widget"}
        )

    def test_item_not_found(self):
        resp = self.client.get("/items/999")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), {"detail": "Item not found"})
