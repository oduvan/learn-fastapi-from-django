from fastapi import FastAPI

from app.routers import items, users

app = FastAPI(title="Project Structure (FastAPI)")

app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "It works!"}
