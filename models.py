from sqlalchemy import Column, Integer, String, UniqueConstraint
from database import Base

class ApiTarget(Base):
    __tablename__ = "api_target"
    __table_args__ = (
        UniqueConstraint("userId", "id", name="uq_userId_id"),
        {"schema": "api_target"},
    )

    userId = Column("userId", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
