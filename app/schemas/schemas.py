from pydantic import BaseModel
from typing import List, Optional

class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: int

class SpyCatCreate(SpyCatBase):
    pass

class SpyCatUpdate(BaseModel):
    salary: int

class SpyCatResponse(SpyCatBase):
    id: int
    
    class Config:
        from_attributes = True

class TargetBase(BaseModel):
    name: str
    country: str

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None

class TargetResponse(TargetBase):
    id: int
    notes: str
    is_completed: bool
    
    class Config:
        from_attributes = True

class MissionBase(BaseModel):
    targets: List[TargetCreate]

class MissionCreate(MissionBase):
    pass

class MissionUpdate(BaseModel):
    cat_id: Optional[int] = None

class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    is_completed: bool
    targets: List[TargetResponse]
    
    class Config:
        from_attributes = True
