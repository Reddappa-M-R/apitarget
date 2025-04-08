from fastapi import FastAPI
import os
import sys
import uvicorn
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from endpoints import api_router
from auth import auth_router
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError



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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error at {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong. Please try again later."}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url.path}: {exc}")
    return await http_exception_handler(request, exc)

@app.get("/")
def root():
    logger.info("Root path hit")
    return {"message": "Welcome to FastAPI on Vercel!"}

# Required for Vercel deployment
if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8008, reload=True)