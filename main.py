from fastapi import FastAPI
from database import Base, engine
from auth import auth_router
from endpoints import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure & Public API Demo")

app.include_router(auth_router)
app.include_router(api_router)
