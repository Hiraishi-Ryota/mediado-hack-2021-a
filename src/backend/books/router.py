from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form

from .crud import *
from .schemas import *
from db import SessionLocal
from utils.upload import upload

from ebook_split.ebook_split import parse_ebook, get_text_by_path
from nlp.doc2vec import *

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/books/", response_model=BookCreateConfirm)
def pre_add_book(e_pub: UploadFile = File(...), price: int = Form(...)):
    """epubを保存＆分解"""
    e_pub_path = upload(filename=e_pub.filename, file=e_pub.file, dir="static/bibi-bookshelf")
    return parse_ebook(e_pub_path, price)


@router.post("/books/confirm", response_model=BookDetail)
def add_book(book: BookCreateConfirm, db: Session = Depends(get_db)):
    """本の追加"""
    db_book = create_book(db=db, book=book)
    for chapter in book.chapters:
        # TODO テキスト取得
        db_chapter = create_chapter(db=db, chapter=chapter, book_id=db_book.id)
        db_book.chapters.append(db_chapter)
        add_vector(str(db_chapter.id), get_text_by_path(db_chapter.e_pub))
    return db_book


@router.get("/books/", response_model=List[Book])
def all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """本の一覧"""
    books = get_books(db, skip=skip, limit=limit)
    return books


@router.get("/books/{book_id}", response_model=BookDetail)
def find_book(book_id: int, db: Session = Depends(get_db)):
    """本の詳細"""
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/chapters/recommend/{chapter_id}", response_model=List[RecommendChapter])
def recommend_chapter(chapter_id: int, db: Session = Depends(get_db)):
    """おすすめの章"""
    chapter_ids = list(map(int, search_vector(str(chapter_id), 5)))
    db_chapters = []
    for id in chapter_ids:
        db_chapters.append(get_recommend_chapter(db, chapter_id=id))
    return db_chapters
