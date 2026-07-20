from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.db import FakePool


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: open the resource once, before any request is served.
    app.state.pool = FakePool()
    yield
    # Shutdown: close it once, after the last request.
    app.state.pool.close()


app = FastAPI(title="Application Lifespan (FastAPI)", lifespan=lifespan)


@app.get("/users")
def list_users(request: Request):
    return {"users": request.app.state.pool.get_users()}


@app.get("/health")
def health():
    return {"status": "ok"}
