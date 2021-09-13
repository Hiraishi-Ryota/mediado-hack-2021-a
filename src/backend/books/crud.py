from sqlalchemy.orm import Session

from . import models, schemas


def get_book(db: Session, book_id: int):
  return db.query(models.Book).filter(models.Book.id == book_id).first()

# def get_book_by_title(db: Session, title: str):
#   return db.query(models.Book).filter(models.Book.title == title).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
  books = db.query(
    models.Book.id,
    models.Book.title,
    models.Book.price,
    models.Book.author,
    models.Book.cover_img,
  ).offset(skip).limit(limit).all()
  return books

def create_book(db: Session, book: schemas.BookCreateConfirm):
  # TODO **book.dict()による方法
  db_book = models.Book(
    title = book.title,
    price = book.price,
    author = book.author,
    word_count = book.word_count,
    e_pub = book.e_pub,
    cover_img = book.cover_img,
  )
  db.add(db_book)
  db.commit()
  db.refresh(db_book)
  return db_book

def get_chapters(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Chapter).offset(skip).limit(limit).all()

def create_chapter(db: Session, chapter: schemas.ChapterCreate, book_id: int, matrix_row: float):
  db_chapter = models.Chapter(**chapter.dict(), book_id=book_id, matrix_row=matrix_row)
  db.add(db_chapter)
  db.commit()
  db.refresh(db_chapter)
  return db_chapter
