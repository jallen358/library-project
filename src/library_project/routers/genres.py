from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..models import Genre
from ..database import get_session

router=APIRouter(prefix="/genre", tags=["genres"])

@router.post("")
def create_genre(genre: Genre, session: Session = Depends(get_session)): 
    session.add(genre)
    session.commit()
    session.refresh(genre)
    return genre