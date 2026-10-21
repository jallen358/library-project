## File that contains the sqlmodel models
from sqlmodel import Field, Relationship, SQLModel
from datetime import date
from typing import Optional

class Book(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    title : str = Field(index=True) 
    author_id : int = Field(foreign_key="author.id") ## Not sure
    genre_id : int = Field(foreign_key="genre.id")
    author : "Author" = Relationship(back_populates="books")
    genre : "Genre" = Relationship(back_populates="books")
    shelf : Optional["Shelf"] = Relationship(back_populates="books")
    shelf_id: int | None = Field(default=None, foreign_key="shelf.id")
    isbn : str = Field(max_length=13)
    description: str | None = Field(default = None)
    
class Author(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str 
    biography : str
    books : list["Book"] = Relationship(back_populates="author")

class Genre(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    books : list["Book"] = Relationship(back_populates="genre")

class Shelf(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    location : str
    books : list["Book"] = Relationship(back_populates="shelf")
    
class Member(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str # Could use FN and LN
    contact_information : str # TN/Email
    
class Book_Transaction(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    book_id : int = Field(foreign_key="book.id", index=True)
    member_id : int = Field(foreign_key="member.id", index=True)
    checkout_date : date = Field(default_factory=date.today)
    due_date : date | None = None
    return_date : date | None = Field(default=None)
    status : str = "checked out" ## Best practice would be a separate statuses table 
    
