"""
Business Logic helper functions
"""

from sqlmodel import Session, select 
from .models import Book, Book_Transaction

def get_checked_out_books_list(session: Session, member_id: int) -> list[str]:
    statement = (
        select(Book.title)
        .join(Book_Transaction, Book_Transaction.book_id == Book.id)
        .where(Book_Transaction.member_id == member_id)
    )
    return list(session.exec(statement).all())

def get_available_library_inventory(session: Session) -> list[str]:
    checked_out = select(Book_Transaction.book_id).where(Book_Transaction.status != "checked out")
    statement = (
        select(Book.title).where(Book.id.not_in(checked_out))
    )
    return list(session.exec(statement).all())