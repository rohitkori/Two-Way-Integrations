from fastapi import APIRouter, Request, HTTPException
import stripe
from settings import Settings
from utils import publish_customer_event

router = APIRouter()
settings = Settings()

stripe.api_key = settings.stripe_api_key
endpoint_secret = settings.stripe_endpoint_secret

@router.post("/stripe")
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
        
        # Add to Kafka queue to be synced to our database
        publish_customer_event(stripe_customer, 'create', settings.inward_sync_kafka_topic)

    return {"status": "success"}