from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import ApiTarget, ActTableFull
from typing import List
from schemas import ApiTargetCreate, ActTableFullCreate
from auth import get_current_user
from logger import logger
from sqlalchemy.exc import SQLAlchemyError

logger.debug("Debug log")
logger.info("Info log")
logger.warning("Warning log")
logger.error("Error log")

api_router = APIRouter()

@api_router.post("/secure/api_target")
def create_target_secure(
    data: List[ApiTargetCreate],
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    inserted = []
    skipped = []

    try:
        for entry in data:
            exists = db.query(ApiTarget).filter_by(userId=entry.userId, id=entry.id).first()
            if exists:
                logger.warning(f"Duplicate skipped: userId={entry.userId}, id={entry.id}")
                skipped.append(entry)
                continue
            new_target = ApiTarget(**entry.dict())
            db.add(new_target)
            db.flush()  # flush to get primary key if needed
            inserted.append(entry)

        db.commit()
        logger.info(f"{len(inserted)} records inserted by {current_user}, {len(skipped)} skipped")
        return {
            "inserted_count": len(inserted),
            "skipped_count": len(skipped),
            "inserted": inserted,
            "skipped": skipped
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error during bulk insert: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        logger.exception(f"Unexpected error during bulk insert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.post("/public/api_target")
def create_target_public(data: List[ApiTargetCreate], db: Session = Depends(get_db)):
    inserted = []
    skipped = []

    try:
        for entry in data:
            exists = db.query(ApiTarget).filter_by(userId=entry.userId, id=entry.id).first()
            if exists:
                logger.warning(f"Duplicate skipped: userId={entry.userId}, id={entry.id}")
                skipped.append(entry)
                continue
            new_entry = ApiTarget(**entry.dict())
            db.add(new_entry)
            db.flush()
            inserted.append(entry)

        db.commit()
        logger.info(f"Public bulk insert done. Inserted: {len(inserted)}, Skipped: {len(skipped)}")
        return {
            "inserted_count": len(inserted),
            "skipped_count": len(skipped),
            "inserted": inserted,
            "skipped": skipped
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/secure/act_full_table")
def create_act_secure(
    data: List[ActTableFullCreate],
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    inserted = []
    skipped = []

    try:
        for entry in data:
            exists = db.query(ActTableFull).filter_by(act_id=entry.act_id).first()
            if exists:
                logger.warning(f"Duplicate skipped: act_id={entry.act_id}")
                skipped.append(entry)
                continue
            new_target = ApiTarget(**entry.dict())
            db.add(new_target)
            db.flush()  # flush to get primary key if needed
            inserted.append(entry)

        db.commit()
        logger.info(f"{len(inserted)} records inserted by {current_user}, {len(skipped)} skipped")
        return {
            "inserted_count": len(inserted),
            "skipped_count": len(skipped),
            "inserted": inserted,
            "skipped": skipped
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error during bulk insert: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        logger.exception(f"Unexpected error during bulk insert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.post("/public/act_full_table")
def create_act_public(data: List[ActTableFullCreate], db: Session = Depends(get_db)):
    inserted = []
    skipped = []

    try:
        for entry in data:
            exists = db.query(ActTableFull).filter_by(act_id=entry.act_id).first()
            if exists:
                logger.warning(f"Duplicate skipped: act_id={entry.act_id}")
                skipped.append(entry)
                continue
            new_entry = ActTableFull(**entry.dict())
            db.add(new_entry)
            db.flush()
            inserted.append(entry)

        db.commit()
        logger.info(f"Public bulk insert done. Inserted: {len(inserted)}, Skipped: {len(skipped)}")
        return {
            "inserted_count": len(inserted),
            "skipped_count": len(skipped),
            "inserted": inserted,
            "skipped": skipped
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

