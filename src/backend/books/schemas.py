from typing import List, Optional

from pydantic import BaseModel


class ChapterBase(BaseModel):
    title: str
    price: int
    author: str
    e_pub: str
    word_count: int


class ChapterCreate(ChapterBase):
    chapter_num: int
    pass


class Chapter(ChapterBase):
    id: int
    chapter_num: int
    book_id: int

    class Config:
        orm_mode = True


class RecommendChapter(Chapter):
    book_title: str
    book_author: str


class BookCreateConfirm(ChapterBase):
    cover_img: str
    chapters: List[ChapterCreate] = []


class Book(BaseModel):
    id: int
    title: str
    price: int
    author: str
    cover_img: str


class BookDetail(Book):
    e_pub: str
    word_count: int
    chapters: List[Chapter] = []

    class Config:
        orm_mode = True
