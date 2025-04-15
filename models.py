from sqlalchemy import Column, Integer, String, UniqueConstraint, Float, Date
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

class ActTableFull(Base):
    __tablename__ = "act_table_full"
    __table_args__ = (
        UniqueConstraint("act_id", name="unique_act_id"),
        {"schema": "api_target"},
    )
    act_id = Column("act_id", Integer, primary_key=True)
    struct_id = Column(Integer)
    target_id = Column(Integer)
    target_name = Column(String)
    target_class = Column(String)
    accession = Column(String)
    gene = Column(String)
    swissprot = Column(String)
    act_value = Column(Float)
    act_unit = Column(String)
    act_type = Column(String)
    act_comment = Column(String)
    act_source = Column(String)
    relation = Column(String)
    moa = Column(Integer)
    moa_source = Column(String)
    act_source_url = Column(String)
    moa_source_url = Column(String)
    action_type = Column(String)
    first_in_class = Column(Integer)
    tdl = Column(String)
    act_ref_id = Column(Integer)
    moa_ref_id = Column(Integer)
    organism = Column(String)
    date = Column(Date)