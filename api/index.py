from fastapi import FastAPI
from auth import auth_router
from endpoints import api_router
from fastapi.middleware.cors import CORSMiddleware

from logger import logger  # your logger setup

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # secure later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(api_router)

# ✅ Required by Vercel: Expose the app object
handler = app

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Hello from FastAPI on Vercel!"}
