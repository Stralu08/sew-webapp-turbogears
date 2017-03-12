# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from sewwebappturbogear import model
from sewwebappturbogear.controllers.secure import SecureController
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


__all__ = ['RootController']


class BookController(EasyCrudRestController):
    model = Book


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
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    books = BookController(DBSession)


    def _before(self, *args, **kw):
        tmpl_context.project_name = "sewwebappturbogear"

    @expose('sewwebappturbogear.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')
    @expose('sewwebappturbogear.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('sewwebappturbogear.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('sewwebappturbogear.templates.data')
    @expose('json')
    def data(self, **kw):
        """
        This method showcases how you can use the same controller
        for a data page and a display page.
        """
        return dict(page='data', params=kw)
    @expose('sewwebappturbogear.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('sewwebappturbogear.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('sewwebappturbogear.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)

    @expose("sewwebappturbogear.templates.book")
    def test(self):
        print("test")
        books = DBSession.query(Book)
        for book in books:
            print(book.title)
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
