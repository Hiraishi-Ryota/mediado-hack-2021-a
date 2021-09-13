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


class BookBase(BaseModel):
  # title: str
  price: int


class BookCreate(BookBase):
  e_pub: str


class Book(BookBase):
  id: int

  chapters: List[Chapter] = []

  class Config:
    orm_mode = True
