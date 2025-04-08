from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ApiTarget
from schemas import ApiTargetCreate
from auth import get_current_user
from logger import logger

logger.info("Authentication successful")
logger.error("Failed to fetch record")


api_router = APIRouter()

@api_router.post("/secure/api_target")
def create_target_secure(
    data: ApiTargetCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    target = ApiTarget(**data.dict())
    db.add(target)
    db.commit()
    db.refresh(target)
    return {
        "message": "Data inserted (secure)",
        "inserted_by": current_user,
        "data": data
    }

@api_router.post("/public/api_target")
def create_target_public(
    data: ApiTargetCreate,
    db: Session = Depends(get_db)
):
    target = ApiTarget(**data.dict())
    db.add(target)
    db.commit()
    db.refresh(target)
    return {
        "message": "Data inserted (public)",
        "data": data
    }
