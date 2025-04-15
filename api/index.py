from fastapi import FastAPI
import os
import sys
import uvicorn
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from endpoints import api_router
from auth import auth_router
from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException



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

async def general_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return await http_exception_handler(request, exc)

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error on {request.url} - {exc}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Request validation failed",
            "details": exc.errors()
        }
    )
# Validation handler (422 Unprocessable Entity)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return await request_validation_exception_handler(request, exc)
app.add_exception_handler(StarletteHTTPException, general_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
@app.get("/")
def root():
    logger.info("Root path hit")
    return {"message": "Welcome to FastAPI on Vercel!"}

# Required for Vercel deployment
if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8013, reload=True)