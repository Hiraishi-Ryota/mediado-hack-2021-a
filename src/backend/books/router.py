from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form

from .crud import *
from .schemas import *
from db import SessionLocal
from utils.upload import upload


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
    e_pub_path = upload(filename=e_pub.filename, file=e_pub.file, dir="static/bookshelf")

    # EpubSplit(e_pub_path).split_book()

    # TODO epub parse
    dummy_chapter = ChapterCreate(
        title="",
        price=0,
        author="",
        e_pub="",
        word_count=0
    )
    book = BookCreateConfirm(
        title="",
        price=price,
        author="",
        cover_img="",
        word_count=0,
        e_pub=e_pub_path,
        chapters=[dummy_chapter] * 3
    )
    return book


@router.post("/books/confirm", response_model=BookDetail)
def add_book(book: BookCreateConfirm, db: Session = Depends(get_db)):
    """本の追加"""
    db_book = create_book(db=db, book=book)
    for chapter in book.chapters:
        # TODO GET ベクトル
        matrix_row = 0
        db_book.chapters.append(create_chapter(db=db, chapter=chapter, book_id=db_book.id, matrix_row=matrix_row))
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
    db_chapters = get_recommend_chapters(db, chapter_id=chapter_id)
    if len(db_chapters) == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_chapters
