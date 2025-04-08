from fastapi import FastAPI
from endpoints import api_router
from auth import auth_router
from fastapi.middleware.cors import CORSMiddleware
from logger import logger

logger.debug("Debug log")
logger.info("Info log")
logger.warning("Warning log")
logger.error("Error log")


app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Required for Vercel deployment
handler = app
