from fastapi import APIRouter, Depends
from ..models import Author
from sqlmodel import Session

from ..database import get_session

router = APIRouter(prefix="/author", tags=["authors"])

@router.post("")
def create_author(author: Author, session: Session = Depends(get_session)):
    session.add(author)
    session.commit()
    session.refresh(author)
    return author