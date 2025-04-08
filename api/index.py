from fastapi import FastAPI
from endpoints import api_router
import logging
from logger import logger

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(api_router)

@app.get("/")
def root():
    logger.info("Root path hit")
    return {"message": "Welcome to FastAPI on Vercel!"}

# ✅ THIS IS REQUIRED FOR VERCEL TO DETECT THE ASGI APP
handler = app
