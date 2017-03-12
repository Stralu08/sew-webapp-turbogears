from sewwebappturbogear.model import DBSession
from sewwebappturbogear.model.book import Book
from sprox.formbase import AddRecordForm
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller


class AddBookForm(AddRecordForm):
    __model__ = Book
    __require_fields__ = ['isbn10', 'author', 'title']
    __field_order__ = ['title', 'author', 'isbn10', 'isbn13',]

add_book_form = AddBookForm(DBSession)


class BookTable(TableBase):
    __model__ = Book
    #__limit_fields__ = ['isbn10', 'isbn13']

book_table = BookTable(DBSession)


class BookTableFiller(TableFiller):
    __model__ = Book
    #__limit_fields__ = ['isbn10', 'isbn13', 'author', 'title']

book_table_filler = BookTableFiller(DBSession)