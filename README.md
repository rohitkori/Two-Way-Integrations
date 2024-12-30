# Two-way Integrations

### This project consists of a FastAPI server and 2 workers:
- FastAPI server for managing customers in MySQL database and publishing sync events
- `customer_inward_sync_worker.py` - Syncs customers from Stripe to our database
- `customer_outward_sync_worker.py` - Syncs customers from our database to Stripe

## Setup Instructions:

1. Create virtual environment:
    ```
    pipenv shell
    ```

2. Install dependencies:
    ```
    pipenv install
    ```

3. Configure environment variables:
    ```
    cp .env.example .env
    # Update .env with your values
    ```

4. Start the Kafka and Zookeeper(using docker-compose):
    ```
    docker compose up -d 
    ```

5. Start the services:

    a. Start FastAPI server:
    ```
    uvicorn main:app --port 8000
    ```

    b. Start outward sync worker (new terminal):
    ```
    python customer_outward_sync_worker.py
    ```

    c. Start inward sync worker (new terminal):
    ```
    python customer_inward_sync_worker.py
    ```

6. Set up Stripe webhook:
    ```
    # Install and run ngrok
    ngrok http http://localhost:8000
    ```
    Take the generated URL and configure it in your Stripe dashboard as a webhook endpoint for customer events.