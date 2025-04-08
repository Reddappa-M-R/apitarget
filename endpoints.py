import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ApiTarget
from schemas import ApiTargetCreate
from auth import get_current_user

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

api_router = APIRouter()

# 🔐 Secure API
@api_router.post("/secure/api_target")
def create_target_secure(data: ApiTargetCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    logger.info(f"Inserting secure data for user {user}: {data}")
    target = ApiTarget(**data.dict())
    db.add(target)
    db.commit()
    logger.info("Secure data inserted successfully.")
    return {"msg": "Data inserted (secure)", "data": data}

# 🌐 Public API
@api_router.post("/public/api_target")
def create_target_public(data: ApiTargetCreate, db: Session = Depends(get_db)):
    logger.info(f"Inserting public data: {data}")
    target = ApiTarget(**data.dict())
    db.add(target)
    db.commit()
    logger.info("Public data inserted successfully.")
    return {"msg": "Data inserted (public)", "data": data}
