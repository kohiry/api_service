import uvicorn
from fastapi import FastAPI

app = FastAPI(title="api service for create users")


@app.post("/new")
def new_users():
    return "1"


@app.get("/all")
def new_users():
    return "1"


@app.delete("/{uuid}")
def new_users(uuid):
    return "1"


@app.get("/{uuid}")
def new_users(uuid):
    return "1"


@app.get("/{count}")
def new_users(count):
    return "1"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
