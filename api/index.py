from fastapi import FastAPI
from database import Base, engine
from auth import auth_router
from endpoints import api_router
from logger import logger  # 👈 custom logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure & Public API Demo")

app.include_router(auth_router)
app.include_router(api_router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Entry for Vercel
handler = app

@handler.get("/")
def read_root():
    logger.info("Root endpoint hit")  # ✅ Example logging
    return {"message": "Hello from FastAPI on Vercel!"}
