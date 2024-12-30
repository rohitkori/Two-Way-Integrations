from sqlmodel import Session, create_engine, SQLModel
from settings import Settings

settings = Settings()

engine = create_engine(settings.database_url)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session