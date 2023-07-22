import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from database import engine
from models import ItemCreate, User

app = FastAPI(title="api service for create users")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/new")
def create_items(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = User(uuid=item.uuid, text=item.text)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item create successfully", "item": db_item}


@app.get("/all")
def new_users():
    return "1"


@app.delete("/{uuid}")
def delete_item(uuid: str, db: Session = Depends(get_db)):
    db_item = (
        db.query(User).filter(User.uuid == uuid).first()
    )  # becouse if just "get", we can have error
    if db_item:
        db.delete(db_item)
        db.commit()
        return {"message": "Item deleted successfully"}
    else:
        return {"message": "Item not found"}


@app.get("/{uuid}")
def new_users(uuid):
    return "1"


@app.get("/{count}")
def new_users(count):
    return "1"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
