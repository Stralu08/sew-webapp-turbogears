from sqlalchemy import *

from sewwebappturbogear.model import DeclarativeBase


class Book(DeclarativeBase):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    isbn10 = Column(Text, unique=True)
    isbn13 = Column(Text, unique=True)
    author = Column(Text)
    title = Column(Text)
    pages = Column(Integer)
    published = Column(Text)
    desc = Column(Text)