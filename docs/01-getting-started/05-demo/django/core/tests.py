from django.test import TestCase


class LifespanTests(TestCase):
    def test_ready_opened_the_pool(self):
        from core import pool

        # AppConfig.ready() ran at startup and opened the pool.
        self.assertIsNotNone(pool.pool)
        self.assertFalse(pool.pool.closed)

    def test_users_served_from_pool(self):
        resp = self.client.get("/users")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            {"users": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Alan"}]},
        )

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "ok"})
