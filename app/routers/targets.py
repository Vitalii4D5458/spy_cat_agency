from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Target
from app.schemas.schemas import TargetUpdate, TargetResponse

router = APIRouter(prefix="/targets", tags=["targets"])

@router.put("/{target_id}", response_model=TargetResponse)
def update_target(target_id: int, target_update: TargetUpdate, db: Session = Depends(get_db)):
    target = db.query(Target).filter(Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    
    if target.is_completed or target.mission.is_completed:
        raise HTTPException(status_code=400, detail="Cannot update notes for completed target or mission")
    
    if target_update.notes is not None:
        target.notes = target_update.notes
    
    if target_update.is_completed is not None:
        target.is_completed = target_update.is_completed
        
        all_targets = db.query(Target).filter(Target.mission_id == target.mission_id).all()
        if all(t.is_completed for t in all_targets):
            target.mission.is_completed = True
    
    db.commit()
    db.refresh(target)
    return target
