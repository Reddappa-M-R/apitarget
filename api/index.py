import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from auth import auth_router
from endpoints import api_router

# -------------------
# Setup Logging
# -------------------
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# -------------------
# FastAPI App
# -------------------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure & Public API Demo")
app.include_router(auth_router)
app.include_router(api_router)

# CORS Middleware for Vercel / frontend use
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vercel handler
handler = app

# -------------------
# Root Route
# -------------------
@handler.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"message": "Hello from FastAPI on Vercel!"}
