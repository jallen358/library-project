from sqlmodel import SQLModel, create_engine, Session
from . import models  # noqa: F401

sqlite_url = "sqlite:///C:/dev/library-project/src/library_project/database.db"

connect_args = {"check_same_thread" : False}
engine = create_engine (sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session