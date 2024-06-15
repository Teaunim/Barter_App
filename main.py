# main.py

from fastapi import FastAPI
import logging

from src.features.offers.routes import offers_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.features.auth.routes import auth_router
    from src.features.profile.routes import profile_router
    from src.features.products.routes import products_router
    # from src.features.messages.routes import messages_router
except ImportError as e:
    logger.error(f"Error importing routers: {e}")
    raise e

app = FastAPI()

try:
    app.include_router(auth_router, prefix="/auth")
    app.include_router(profile_router, prefix="/profile")
    app.include_router(products_router, prefix="/products")
    app.include_router(offers_router, prefix="/offers")
    # app.include_router(messages_router, prefix="/messages")
except Exception as e:
    logger.error(f"Error including routers: {e}")
    raise e


@app.get("/")
def read_root():
    return {"message": "Welcome to the Barter App!"}
