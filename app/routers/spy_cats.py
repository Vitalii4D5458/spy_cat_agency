from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import SpyCat, Mission
from app.schemas.schemas import SpyCatCreate, SpyCatUpdate, SpyCatResponse
from app.services.breed_validator import validate_breed

router = APIRouter(prefix="/spy-cats", tags=["spy-cats"])

@router.post("/", response_model=SpyCatResponse)
async def create_spy_cat(spy_cat: SpyCatCreate, db: Session = Depends(get_db)):
    if not await validate_breed(spy_cat.breed):
        raise HTTPException(status_code=400, detail="Invalid cat breed")
    
    db_spy_cat = SpyCat(**spy_cat.dict())
    db.add(db_spy_cat)
    db.commit()
    db.refresh(db_spy_cat)
    return db_spy_cat

@router.get("/", response_model=List[SpyCatResponse])
def list_spy_cats(db: Session = Depends(get_db)):
    return db.query(SpyCat).all()

@router.get("/{cat_id}", response_model=SpyCatResponse)
def get_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    spy_cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not spy_cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return spy_cat

@router.put("/{cat_id}", response_model=SpyCatResponse)
def update_spy_cat(cat_id: int, spy_cat_update: SpyCatUpdate, db: Session = Depends(get_db)):
    spy_cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not spy_cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    
    spy_cat.salary = spy_cat_update.salary
    db.commit()
    db.refresh(spy_cat)
    return spy_cat

@router.delete("/{cat_id}")
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    spy_cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not spy_cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    
    active_missions = db.query(Mission).filter(Mission.cat_id == cat_id).first()
    if active_missions:
        raise HTTPException(status_code=400, detail="Cannot delete spy cat with active missions")
    
    db.delete(spy_cat)
    db.commit()
    return {"message": "Spy cat deleted successfully"}
