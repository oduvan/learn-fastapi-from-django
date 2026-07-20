"""The same stand-in resource as the FastAPI project. It's opened once in
AppConfig.ready() and held in the module-level ``pool`` global.

Note there is no shutdown counterpart: Django has no built-in
process-shutdown hook for application code."""


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


pool: FakePool | None = None
