from kafka import KafkaConsumer
from settings import Settings
import json
import stripe

settings = Settings()

def add_to_stripe(customer):
    stripe.api_key = settings.stripe_api_key

    stripe_customer = stripe.Customer.create(
        name=customer['name'],
        email=customer['email']
    )

    print("Stripe customer updated!!")

def consumer_outwards_sync(topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=settings.kafka_url,
    )

    for message in consumer:
        message_str = message.value.decode('utf-8')
        message_data = json.loads(message_str)
        print("message_data: ", message_data)

        add_to_stripe(message_data['customer'])

consumer_outwards_sync('system_to_stripe')