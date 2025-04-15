from typing import Optional
from pydantic import BaseModel
from datetime import date



class ApiTargetCreate(BaseModel):
    userId: int
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None


class ActTableFullCreate(BaseModel):
    act_id: int
    struct_id: Optional[int] = None
    target_id: Optional[int] = None
    target_name: Optional[str] = None
    target_class: Optional[str] = None
    accession: Optional[str] = None
    gene: Optional[str] = None
    swissprot: Optional[str] = None
    act_value: Optional[float] = None
    act_unit: Optional[str] = None
    act_type: Optional[str] = None
    act_comment: Optional[str] = None
    act_source: Optional[str] = None
    relation: Optional[str] = None
    moa: Optional[int] = None
    moa_source: Optional[str] = None
    act_source_url: Optional[str] = None
    moa_source_url: Optional[str] = None
    action_type: Optional[str] = None
    first_in_class: Optional[int] = None
    tdl: Optional[str] = None
    act_ref_id: Optional[int] = None
    moa_ref_id: Optional[int] = None
    organism: Optional[str] = None
    date: Optional[str] = None