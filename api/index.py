from fastapi import FastAPI
from auth import auth_router
from endpoints import api_router
from logger import logger
from fastapi.middleware.cors import CORSMiddleware

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
def read_root():
    return {"message": "FastAPI on Vercel is working!"}

# ✅ THIS IS REQUIRED FOR VERCEL TO DETECT THE ASGI APP
handler = app
