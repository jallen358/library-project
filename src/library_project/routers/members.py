from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..models import Member
from ..database import get_session

router = APIRouter(prefix="/member",tags=["members"])

@router.post("")
def create_member(member: Member, session : Session = Depends(get_session)):
    session.add(member)
    session.commit()
    session.refresh(member)
    return member