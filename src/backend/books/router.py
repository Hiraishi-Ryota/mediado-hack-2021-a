from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, File, UploadFile, Form
from pathlib import Path
import shutil
from sqlalchemy.orm import Session
from tempfile import NamedTemporaryFile

from .crud import *
from .models import *
from .schemas import *
from db import SessionLocal


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/books/", response_model=schemas.Book)
def save_upload_file_tmp(e_pub: UploadFile=File(...), price: int=Form(...), db: Session = Depends(get_db)):
  """epubを保存し、dbに追加"""
  e_pub_path:Path = ""
  try:
    with NamedTemporaryFile(delete=False, suffix=Path(e_pub.filename).suffix) as tmp:
      shutil.copyfileobj(e_pub.file, tmp)
      e_pub_path = Path(tmp.name)
  finally:
    e_pub.file.close()
  print(type(e_pub_path))
  print(type("test"))
  book = schemas.BookCreate(
    price = price,
    e_pub = str(e_pub_path),
  )
  return create_book(db=db, book=book)

# def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
#     db_book = crud.get_book_by_email(db, email=book.email)
#     if db_book:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_book(db=db, book=book)


# @router.get("/books/", response_model=List[schemas.Book])
# def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     books = crud.get_books(db, skip=skip, limit=limit)
#     return books


# @router.get("/books/{book_id}", response_model=schemas.Book)
# def read_book(book_id: int, db: Session = Depends(get_db)):
#     db_book = crud.get_book(db, book_id=book_id)
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return db_book


# @router.post("/books/{book_id}/chapters/", response_model=schemas.Chapter)
# def create_chapter_for_book(
#     book_id: int, chapter: schemas.ChapterCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_book_chapter(db=db, chapter=chapter, book_id=book_id)


# @app.get("/chapters/", response_model=List[schemas.Chapter])
# def read_chapters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     chapters = crud.get_chapters(db, skip=skip, limit=limit)
#     return chapters