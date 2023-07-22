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


# Endpoint для выдачи всех элементов базы данных
@app.get("/all/")
def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(User).offset(skip).limit(limit).all()
    return items


# Endpoint для выдачи конкретной записи из базы данных
@app.get("/{uuid}")
def get_item(uuid: str, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.uuid == uuid).first()
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Record not found")


# Endpoint для выдачи определенного числа записей из базы данных
@app.get("/count/{count}")
def get_items_limit(count: int = 100, db: Session = Depends(get_db)):
    items = db.query(User).limit(count).all()
    return items


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
