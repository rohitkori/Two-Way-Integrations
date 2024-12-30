from kafka import KafkaProducer
from settings import Settings
import json

settings = Settings()

def publish_customer_event(customer, action, topic_name):
    producer = KafkaProducer(bootstrap_servers=settings.kafka_url)

    event = {
        "action": action,
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email
        }
    }

    # convert dict to JSON string and then encoding to bytes
    producer.send(topic_name, json.dumps(event).encode('utf-8'))
    producer.flush()

