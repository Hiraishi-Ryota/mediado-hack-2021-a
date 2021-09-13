from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
import os
from pathlib import Path
import shutil
from sqlalchemy.orm import Session
from tempfile import NamedTemporaryFile
import uuid

from .crud import *
from .models import *
from .schemas import *
from db import SessionLocal


router = APIRouter()

BASE_DIR = os.getcwd()
E_PUB_DIR = "static/bookshelf"

# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/books/", response_model=schemas.BookCreateConfirm)
def pre_add_book(e_pub: UploadFile=File(...), price: int=Form(...), db: Session = Depends(get_db)):
  """epubを保存＆分解"""
  e_pub_path:Path = ""
  try:
    with NamedTemporaryFile(delete=False, suffix=Path(e_pub.filename).suffix, dir=E_PUB_DIR) as tmp:
      shutil.copyfileobj(e_pub.file, tmp)
      e_pub_path = Path(tmp.name)
  finally:
    e_pub.file.close()

  # TODO epub parse
  dummy_chapter = schemas.ChapterBase(
    title = "",
    price = 0,
    author = "",
  )
  book = schemas.BookCreateConfirm(
    title = "",
    price = price,
    author = "",
    cover_img = "",
    word_count = 0,
    e_pub = str(e_pub_path.relative_to(BASE_DIR)),
    chapters = [dummy_chapter]*3
  )
  return book

@router.post("/books/confirm", response_model=schemas.BookDetail)
def add_book(book: schemas.BookCreateConfirm, db: Session = Depends(get_db)):
  """本の追加"""
  db_book = create_book(db=db, book=book)
  for chapter in book.chapters:
    # TODO GET ベクトル
    matrix_row = 0
    db_book.chapters.append(create_chapter(db=db, chapter=chapter, book_id=db_book.id, matrix_row=matrix_row))
  return db_book

@router.get("/books/", response_model=List[schemas.Book])
def all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  """本の一覧"""
  books = get_books(db, skip=skip, limit=limit)
  return books

@router.get("/books/{book_id}", response_model=schemas.BookDetail)
def find_book(book_id: int, db: Session = Depends(get_db)):
  """本の詳細"""
  db_book = get_book(db, book_id=book_id)
  if db_book is None:
      raise HTTPException(status_code=404, detail="Book not found")
  return db_book


# @router.post("/books/{book_id}/chapters/", response_model=schemas.Chapter)
# def create_chapter_for_book(
#     book_id: int, chapter: schemas.ChapterCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_book_chapter(db=db, chapter=chapter, book_id=book_id)


# @app.get("/chapters/", response_model=List[schemas.Chapter])
# def read_chapters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     chapters = crud.get_chapters(db, skip=skip, limit=limit)
#     return chapters
