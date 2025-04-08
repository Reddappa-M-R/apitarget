from fastapi import FastAPI
from database import Base, engine
from auth import auth_router
from endpoints import api_router

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(title="Secure & Public API Demo")

# Include authentication and API routers
app.include_router(auth_router)
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}

# If you have additional routes for authenticated and public APIs, include them here
# or import them from other modules.
