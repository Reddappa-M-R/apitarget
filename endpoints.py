from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ApiTarget
from schemas import ApiTargetCreate
from auth import get_current_user
from logger import logger
from logger import logger

logger.debug("Debug log")
logger.info("Info log")
logger.warning("Warning log")
logger.error("Error log")

api_router = APIRouter()

@api_router.post("/secure/api_target")
def create_target_secure(
    data: ApiTargetCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        target = ApiTarget(**data.dict())
        db.add(target)
        db.commit()
        db.refresh(target)
        logger.info(f"Secure insert by {current_user}")
        return {
            "message": "Data inserted (secure)",
            "inserted_by": current_user,
            "data": data
        }
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/public/api_target")
def create_target_public(
    data: ApiTargetCreate,
    db: Session = Depends(get_db)
):
    try:
        target = ApiTarget(**data.dict())
        db.add(target)
        db.commit()
        db.refresh(target)
        logger.info("Public insert")
        return {
            "message": "Data inserted (public)",
            "data": data
        }
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
