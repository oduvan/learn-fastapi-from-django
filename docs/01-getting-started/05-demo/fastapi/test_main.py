from fastapi.testclient import TestClient

from app.main import app


def test_lifespan_opens_and_closes_the_pool():
    # TestClient runs the lifespan only when used as a context manager.
    with TestClient(app) as client:
        # Startup has run: the pool is open.
        assert app.state.pool.closed is False

        resp = client.get("/users")
        assert resp.status_code == 200
        assert resp.json() == {
            "users": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Alan"}]
        }

        pool = app.state.pool

    # The context has exited: shutdown has run and the pool is closed.
    assert pool.closed is True


def test_health():
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
