from fastapi import FastAPI
from sqlmodel import Session, create_engine, SQLModel
from models import Customer
from settings import Settings

settings = Settings()

engine = create_engine(settings.database_url)

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}