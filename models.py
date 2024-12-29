from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Optional


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

