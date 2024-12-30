from kafka import KafkaConsumer
from settings import Settings
import json
import stripe

settings = Settings()

consumer = KafkaConsumer(
        settings.outward_sync_kafka_topic,
        bootstrap_servers=settings.kafka_url,
    )

def add_to_stripe(customer):
    stripe.api_key = settings.stripe_api_key

    stripe_customer = stripe.Customer.create(
        name=customer['name'],
        email=customer['email']
    )

    print("Stripe customer updated!!")

def main():
    for message in consumer:
        # Decode and then convert to dict
        message_str = message.value.decode('utf-8')
        message_data = json.loads(message_str)

        # can add more functions here for other integrations like salesforce.
        add_to_stripe(message_data['customer']) 

if __name__ == "__main__":
    main()
