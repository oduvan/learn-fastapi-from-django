from fastapi import FastAPI

app = FastAPI(title="Dev Server (FastAPI)")


@app.get("/")
def read_root():
    return {"message": "It works!"}


@app.get("/health")
def health():
    return {"status": "ok"}
