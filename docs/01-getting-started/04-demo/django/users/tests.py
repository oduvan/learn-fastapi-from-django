from django.test import TestCase


class UserTests(TestCase):
    def test_list_users(self):
        resp = self.client.get("/users")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            {"users": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Alan"}]},
        )

    def test_get_user(self):
        self.assertEqual(
            self.client.get("/users/2").json(), {"id": 2, "name": "Alan"}
        )

    def test_user_not_found(self):
        resp = self.client.get("/users/999")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), {"detail": "User not found"})
