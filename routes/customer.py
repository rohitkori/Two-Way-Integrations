from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import Customer
from settings import Settings
from utils import publish_customer_event
from database import get_session

settings = Settings()
router = APIRouter()

@router.get("/get")
async def get_customer(session: Session = Depends(get_session)):
    customers = session.query(Customer).all()
    return customers

@router.post("/create")
async def create_customer(customer: Customer, session: Session = Depends(get_session)):
    if customer.id == 0:
        customer.id = None
    session.add(customer)
    session.commit()
    session.refresh(customer)
    
    publish_customer_event(customer, 'create', settings.outward_sync_kafka_topic)
    
    return customer