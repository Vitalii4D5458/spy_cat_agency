from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Mission, SpyCat, Target
from app.schemas.schemas import MissionCreate, MissionUpdate, MissionResponse

router = APIRouter(prefix="/missions", tags=["missions"])

@router.post("/", response_model=MissionResponse)
async def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    if len(mission.targets) < 1 or len(mission.targets) > 3:
        raise HTTPException(status_code=400, detail="Mission must have between 1 and 3 targets")
    
    db_mission = Mission()
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    
    for target_data in mission.targets:
        db_target = Target(mission_id=db_mission.id, **target_data.dict())
        db.add(db_target)
    
    db.commit()
    db.refresh(db_mission)
    return db_mission

@router.get("/", response_model=List[MissionResponse])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()

@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.put("/{mission_id}/assign", response_model=MissionResponse)
def assign_cat_to_mission(mission_id: int, mission_update: MissionUpdate, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission_update.cat_id:
        cat = db.query(SpyCat).filter(SpyCat.id == mission_update.cat_id).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Spy cat not found")
        
        existing_mission = db.query(Mission).filter(Mission.cat_id == mission_update.cat_id).first()
        if existing_mission:
            raise HTTPException(status_code=400, detail="Cat already has an active mission")
    
    mission.cat_id = mission_update.cat_id
    db.commit()
    db.refresh(mission)
    return mission

@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Cannot delete mission assigned to a cat")
    
    db.delete(mission)
    db.commit()
    return {"message": "Mission deleted successfully"}
