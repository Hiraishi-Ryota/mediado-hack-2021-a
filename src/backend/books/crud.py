from sqlalchemy.orm import Session

from . import models, schemas


def get_book(db: Session, book_id: int):
  return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
      email=book.email,
      hashed_password=fake_hashed_password
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_chapters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chapter).offset(skip).limit(limit).all()


def create_book_chapter(db: Session, chapter: schemas.ChapterCreate, book_id: int):
    db_chapter = models.Chapter(**chapter.dict(), owner_id=book_id)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter
