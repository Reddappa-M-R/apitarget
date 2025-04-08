from sqlalchemy import Column, Integer, String
from database import Base

class ApiTarget(Base):
    __tablename__ = "api_target"
    __table_args__ = {"schema": "api_target", "extend_existing": True}

    userId = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
