from kafka import KafkaConsumer
from sqlalchemy import create_engine, text
from settings import Settings
import json

settings = Settings()

consumer = KafkaConsumer(
    settings.inward_sync_kafka_topic,
    bootstrap_servers=settings.kafka_url,
)

def sync_customer_to_database(customer_data):
    engine = create_engine(settings.database_url)
    connection = engine.connect()
    
    # check if customer exists
    check_query = "SELECT * FROM customer WHERE email = :email"
    result = connection.execute(text(check_query), {
        "email": customer_data['email']
    })
    
    if result.fetchone() is None:
        # Customer doesn't exist, insert new record
        insert_query = "INSERT INTO customer (name, email) VALUES (:name, :email)"
        connection.execute(text(insert_query), {
            "name": customer_data['name'],
            "email": customer_data['email']
        })
        connection.commit()
        print("New customer added from stripe to system...")
    else:
        print("Customer with this email already exists...")

def main():
    for message in consumer:
        # Decode and then convert to dict
        event_str = message.value.decode('utf-8')
        event = json.loads(event_str)
        customer = event['customer']

        sync_customer_to_database(customer)

if __name__ == "__main__":
    main()