from fastapi import FastAPI, Depends, Request, HTTPException
from sqlmodel import Session, create_engine, SQLModel
from models import Customer
from settings import Settings
from utils import producer_outwards_sync
from kafka import KafkaProducer

import stripe
import json

settings = Settings()

engine = create_engine(settings.database_url)

SQLModel.metadata.create_all(engine)

app = FastAPI()

stripe.api_key = settings.stripe_api_key
endpoint_secret = settings.stripe_endpoint_secret
producer = KafkaProducer(bootstrap_servers=settings.kafka_url)


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

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'customer.created':
        stripe_customer = event['data']['object']

        event_payload = {
            "action": "create",
            "customer": {
                "stripe_id": stripe_customer['id'],
                "name": stripe_customer['name'],
                "email": stripe_customer['email']
            }
        }
        producer.send('stripe_to_system', json.dumps(event_payload).encode('utf-8'))
        producer.flush()

    return {"status": "success"}