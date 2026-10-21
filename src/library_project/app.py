from fastapi import FastAPI, Depends, Query
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from datetime import date, timedelta

from .database import create_db_and_tables, get_session
from .models import Book, Genre, Author, Shelf, Book_Transaction, Member

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/book")
def create_book(book: Book, session: Session = Depends(get_session)): 
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.post("/author")
def create_author(author: Author, session: Session = Depends(get_session)):
    session.add(author)
    session.commit()
    session.refresh(author)
    return author

@app.post("/genre")
def create_genre(genre: Genre, session: Session = Depends(get_session)): 
    session.add(genre)
    session.commit()
    session.refresh(genre)
    return genre

@app.post("/shelf")
def create_shelf(shelf: Shelf, session: Session=Depends(get_session)):
    session.add(shelf)
    session.commit()
    session.refresh(shelf)
    return shelf

@app.post("/member")
def create_member(member: Member, session : Session = Depends(get_session)):
    session.add(member)
    session.commit()
    session.refresh(member)
    return member

'''
Get book endpoint using id/title/author: 
'''
@app.get("/book/{book_id}")
def get_book(book_id : int, session: Session=Depends(get_session)):
    book = session.get(Book, book_id)
    if book is None:
        return "Error"
    return book

@app.get("/book")
def get_books(
    author_name: str | None = None, 
    genre : str | None = None,
    limit : int = Query(default= 100, le = 100), 
    session: Session = Depends(get_session)):
    statement = select(Book)
    if author_name: 
        statement = statement.where(Book.author.has(Author.name == author_name))
    if genre:
        statement = statement.where(Book.genre.has(Genre.name.contains(genre)))
    books = session.exec(statement.limit(limit)).all()
    return books

@app.post("/book/checkout")
def checkout_book(book_transaction: Book_Transaction, session: Session = Depends(get_session)):
    book_transaction.checkout_date = date.today()
    book_transaction.due_date = date.today() + timedelta(days = 7)
    book_transaction.status = "checked out"
    book_transaction.return_date = None
    session.add(book_transaction)
    session.commit()
    session.refresh(book_transaction)
    return book_transaction

@app.post("/book/return")
def return_book(book_transaction_id: int, session: Session = Depends(get_session)):
    book_transaction = session.get(Book_Transaction, book_transaction_id)
    book_transaction.status = "returned"
    book_transaction.return_date = date.today()
    session.add(book_transaction)
    session.commit()
    session.refresh(book_transaction)
    return book_transaction

### TODO: A