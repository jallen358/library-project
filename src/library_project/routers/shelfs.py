from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import Shelf

router=APIRouter(prefix="/shelf", tags=["shelves"])

@router.post("/shelf")
def create_shelf(shelf: Shelf, session: Session=Depends(get_session)):
    session.add(shelf)
    session.commit()
    session.refresh(shelf)
    return shelf
