from fastapi import FastAPI

from routes.customer import router as customer_router
from routes.webhook import router as webhook_router


app = FastAPI()

app.include_router(customer_router, prefix="/customer")
app.include_router(webhook_router, prefix="/webhook")