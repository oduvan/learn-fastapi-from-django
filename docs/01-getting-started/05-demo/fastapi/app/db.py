"""A stand-in for a real resource (a database connection pool, an HTTP
client, a loaded model) that must be opened once at startup and closed
once at shutdown."""


class FakePool:
    def __init__(self):
        self.closed = False
        self._users = [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Alan"}]

    def get_users(self):
        if self.closed:
            raise RuntimeError("pool is closed")
        return list(self._users)

    def close(self):
        self.closed = True
