from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import os

from logger import logger

logger.debug("Debug log")
logger.info("Info log")
logger.warning("Warning log")
logger.error("Error log")


auth_router = APIRouter()

USER_DB = {"username": "reddappa", "password": "secret123"}

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.exception(f"Unexpected token error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post("/token", response_model=Token)
def login_for_access_token(user: User):
    try:
        logger.info(f"Login attempt for user: {user.username}")

        if user.username != USER_DB["username"] or user.password != USER_DB["password"]:
            logger.warning(f"Invalid credentials for user: {user.username}")
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        token = create_access_token(data={"sub": user.username})
        logger.info(f"Access token issued for user: {user.username}")

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        logger.exception(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")



