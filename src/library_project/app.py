"""
TODO:  
Delete Books
AI Book Recommendations
Create Routers instead of giant app.py 
"""
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session

from .database import create_db_and_tables, get_session
from .models import Genre, Author, Shelf, Member
from .routers import books, authors, genres, shelfs, members

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(shelfs.router)
app.include_router(members.router)