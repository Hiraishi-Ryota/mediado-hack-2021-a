from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
# from sqlalchemy.orm import Session

# from .books import crud, models, schemas
# from .db import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post("/books/", response_model=schemas.User)
# def create_book(book: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_book = crud.get_book_by_email(db, email=book.email)
#     if db_book:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_book(db=db, book=book)


# @app.get("/books/", response_model=List[schemas.User])
# def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     books = crud.get_books(db, skip=skip, limit=limit)
#     return books


# @app.get("/books/{book_id}", response_model=schemas.User)
# def read_book(book_id: int, db: Session = Depends(get_db)):
#     db_book = crud.get_book(db, book_id=book_id)
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_book


# @app.post("/books/{book_id}/chapters/", response_model=schemas.Chapter)
# def create_chapter_for_book(
#     book_id: int, chapter: schemas.ChapterCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_book_chapter(db=db, chapter=chapter, book_id=book_id)


# @app.get("/chapters/", response_model=List[schemas.Chapter])
# def read_chapters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     chapters = crud.get_chapters(db, skip=skip, limit=limit)
#     return chapters