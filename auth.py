from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import os
from fastapi.security import OAuth2PasswordRequestForm

from logger import logger

auth_router = APIRouter()

# Simulated DB
USER_DB = {"username": "reddappa", "password": "secret123"}

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Models
class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    password: str


# Token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Dependency to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.exception(f"Unexpected token error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Login endpoint
@auth_router.post("/token", response_model=Token)
def login_for_access_token(login_request: User):
    username = login_request.username
    password = login_request.password

    logger.info(f"Login attempt for user: {username}")
    if username != USER_DB["username"] or password != USER_DB["password"]:
        logger.warning(f"Invalid login for user: {username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(data={"sub": username})
    logger.info(f"Issued token for user: {username}")

    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}"}

@auth_router.post("/secure-data")
def read_secure_data(authorization: str = Header(...)):
    try:
        # Extract token from "Bearer <token>"
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return {"message": f"Hello {username}, you are authenticated!"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")