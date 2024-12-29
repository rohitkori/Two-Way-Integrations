from fastapi import FastAPI, Depends
from sqlmodel import Session, create_engine, SQLModel
from models import Customer
from settings import Settings
from utils import producer_outwards_sync

settings = Settings()

engine = create_engine(settings.database_url)

SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/customer/get")
async def get_customer(session: Session = Depends(get_session)):
    customers = session.query(Customer).all()
    return customers

@app.post("/customer/create")
async def create_customer(customer: Customer, session: Session = Depends(get_session)):
    if customer.id == 0:
            customer.id = None
    session.add(customer)
    session.commit()
    session.refresh(customer)
    
    producer_outwards_sync(customer, 'create', 'system_to_stripe')
    
    return customer