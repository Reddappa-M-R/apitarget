from fastapi import FastAPI
from auth import auth_router
from endpoints import api_router
from fastapi.middleware.cors import CORSMiddleware
from logger import logger

app = FastAPI(title="Secure API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set securely in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(api_router)

# ✅ Vercel compatibility
handler = app

@app.get("/")
def root():
    logger.info("Health check hit")
    return {"message": "Hello from FastAPI on Vercel!"}
