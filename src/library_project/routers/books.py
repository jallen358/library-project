from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import date, timedelta
from dotenv import load_dotenv
import anthropic

from .. import services 
from ..database import get_session
from ..models import Book, Book_Transaction, Author, Genre

load_dotenv()
router = APIRouter(prefix="/book", tags=["books"])
client = anthropic.AsyncAnthropic()

@router.get("/{book_id}")
def get_book(book_id : int, session: Session=Depends(get_session)):
    """
    Get book endpoint using id/title/author: 
    """
    book = session.get(Book, book_id)
    if book is None:
        return "Error"
    return book

@router.post("")
def create_book(book: Book, session: Session = Depends(get_session)): 
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.post("/checkout")
def checkout_book(book_transaction: Book_Transaction, session: Session = Depends(get_session)):
    book_transaction.checkout_date = date.today()
    book_transaction.due_date = date.today() + timedelta(days = 7)
    book_transaction.status = "checked out"
    book_transaction.return_date = None
    session.add(book_transaction)
    session.commit()
    session.refresh(book_transaction)
    return book_transaction

@router.post("/return")
def return_book(book_transaction_id: int, session: Session = Depends(get_session)):
    book_transaction = session.get(Book_Transaction, book_transaction_id)
    book_transaction.status = "returned"
    book_transaction.return_date = date.today()
    session.add(book_transaction)
    session.commit()
    session.refresh(book_transaction)
    return book_transaction

@router.post("/recommendations")
async def get_book_recommendations(member_id: int,
                             session: Session = Depends(get_session)):
    member_books_list = services.get_member_books_list(session, member_id)
    available_library_inventory= services.get_available_library_inventory(session)
    # Best practice would be to use a separate function to call claude
    message = f"""Based on the history of reading these books: {member_books_list}, 
    list 1-3 books to read next. 
    The books that you can choose from are: {available_library_inventory}
    """
    try: 
        response = await client.messages.create(
            model = "claude-haiku-5-5",
            max_tokens=500,
            output_config={"effort" : "low"},
            system="You are a librarian that is recommending a new book based on past reading",
            messages = [{"role" : "user", "content": message}])
        return {
            "response" : response.content[0].text, 
            "stop_reason" : response.stop_reason
        }
    except:
        return "Error"
    
@router.get("/{member_id}")
def get_member_books_list(member_id : int):
    return get_member_books_list(member_id)
    
@router.get("")
def get_books(
    author_name: str | None = None, 
    genre : str | None = None,
    limit : int = Query(default= 100, le = 100), 
    session: Session = Depends(get_session)):
    statement = select(Book)
    if author_name: 
        statement = statement.where(Book.author.has(Author.name.icontains(author_name)))
    if genre:
        statement = statement.where(Book.genre.has(Genre.name.icontains(genre)))
    books = session.exec(statement.limit(limit)).all()
    return books

@router.delete("/{book_id}")
def delete_book(
    book_id : int, session: Session = Depends(get_session)
):
    statement = select(Book).where(Book.id == book_id)
    book_to_delete = session.exec(statement).one()
    session.delete(book_to_delete)
    session.commit()
    return book_to_delete
