from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36))
    text = Column(String(16))


# Схема данных для запроса
class ItemCreate(BaseModel):
    uuid: str
    text: str
