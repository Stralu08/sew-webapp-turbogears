# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from sewwebappturbogear import model
from sewwebappturbogear.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from sewwebappturbogear.lib.base import BaseController
from tg import RestController
from tgext.crud import EasyCrudRestController
from sewwebappturbogear.controllers.error import ErrorController
from sewwebappturbogear.forms.book_forms import add_book_form
from sewwebappturbogear.model.book import Book
from sewwebappturbogear.forms.book_forms import book_table
from sewwebappturbogear.forms.book_forms import book_table_filler

from formencode.validators import String, Int, Regex


__all__ = ['RootController']


class BookController(EasyCrudRestController):
    model = Book

    __form_options__ = {
        '__field_validators__': {'title': String(min=3), 'author': String(min=3), 'pages': Int(min=1),
                                 'isbn10': Regex("^\d{10}$"), 'isbn13': Regex("^\d{3}-\d{10}$")},
    }


class RootController(BaseController):
    """
    The root controller for the sew-webapp-turbogear application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    #secc = SecureController()
    #admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    books = BookController(DBSession)

    def _before(self, *args, **kw):
        tmpl_context.project_name = "sewwebappturbogear"

    @expose("sewwebappturbogear.templates.book")
    def test(self):
        books = DBSession.query(Book)
        return dict(books=books)

    @expose('sewwebappturbogear.templates.addbook')
    def add(self, **kw):
        tmpl_context.widget = add_book_form
        return dict(value=kw)

    @expose('sewwebappturbogear.templates.booktable')
    def booktable(self, **kw):
        return dict(table=book_table(value=book_table_filler.get_value()))

    @expose('sewwebappturbogear.templates.oldtable')
    def get_all(self):
        tmpl_context.widget = book_table
        return dict()
