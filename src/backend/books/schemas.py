from typing import List, Optional

from pydantic import BaseModel


class ChapterBase(BaseModel):
  title: str
  price: int
  author: str


class ChapterCreate():
  pass


class Chapter(ChapterBase):
  id: int
  book_id: int

  class Config:
    orm_mode = True


class BookCreateConfirm(BaseModel):
  title: str
  price: int
  author: str
  cover_img: str
  price: int
  e_pub: str
  word_count: int
  chapters: List[ChapterBase] = []


class BookCreate(BaseModel):
  e_pub: str


class Book(BaseModel):
  id: int
  title: str
  price: int
  author: str
  cover_img: str
  price: int


class BookDetail(Book):
  e_pub: str
  word_count: int
  chapters: List[Chapter] = []

  class Config:
    orm_mode = True
