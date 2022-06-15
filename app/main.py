from fastapi import FastAPI

from app.router.payments import router as payments_router
from app.router.postal_codes import router as postal_codes_router

app = FastAPI(title="Cool geo app API", version="0.1.0")
app.include_router(postal_codes_router)
app.include_router(payments_router)
