from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float

from db import BasicModel


class Book(BasicModel):
    __tablename__ = "books"

    title = Column(String, nullable=False, index=True, comment='タイトル')
    price = Column(Integer, nullable=False, index=True, comment='値段(税抜き)')
    author = Column(String, nullable=False, index=True, comment='著者')
    word_count = Column(Integer, comment='文字数')
    e_pub = Column(String, nullable=False, index=True, comment='ePubデータ保存先')
    cover_img = Column(String, nullable=False, index=True, comment='ePubデータ保存先')

    chapters = relationship("Chapter", back_populates="book")


class Chapter(BasicModel):
    __tablename__ = "chapters"

    title = Column(String, nullable=False, index=True, comment='タイトル')
    price = Column(Integer, nullable=False, index=True, comment='値段(税抜き)')
    author = Column(String, index=True, comment='著者')
    word_count = Column(Integer, comment='文字数')
    e_pub = Column(String, nullable=False, index=True, comment='ePubデータ保存先')
    matrix_row = Column(Float, nullable=False, index=True, comment='内容傾向マトリックスの行番号')
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="chapters")
