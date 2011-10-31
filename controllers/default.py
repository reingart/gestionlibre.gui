# -*- coding: utf-8 -*- 
from gluon import *
import gluon

import gluon.validators

from gui2py.form import EVT_FORM_SUBMIT

import config
db = config.db
session = config.session
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index(evt, args = [], vars = {}):
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    
    Project's index page (incomplete)
    """
    # A("GestionLibre", _href="http://code.google.com/p/gestionlibre/"),
    links = UL(*[LI(a) for a in [
    A(B("Customer control panel"), _href=URL(a="gestionlibre", c='crm',f='customer_panel')),
    A(B("Movements panel"), _href=URL(a="gestionlibre", c='operations',f='index')),
    A(B("RIA Stock"), _href=URL(a="gestionlibre", c='scm',f='ria_stock')),
    A(B("Journal entries"), _href=URL(a="gestionlibre", c='accounting',f='journal_entries')),
    A(B("Order allocation"), _href=URL(a="gestionlibre", c='operations',f='order_allocation')),
    A(B("Order allocation list"), _href=URL(a="gestionlibre", c='operations',f='list_order_allocations')),
    A(B("Packing slip"), _href=URL(a="gestionlibre", c='operations',f='packing_slip')),
    A(B("RIA Product billing"), _href=URL(a="gestionlibre", c='operations',f='ria_product_billing_start')),
    A(B("Current account report"), _href=URL(a="gestionlibre", c='crm',f='current_account_report')),
    A(B("Movements list"), _href=URL(a="gestionlibre", c='operations',f='movements_list')),
    A(B("New operation (movements form)"), _href=URL(a="gestionlibre", c='operations',f='movements_start')),
    A(B("Current accounts payments"), _href=URL(a="gestionlibre", c='financials',f='current_accounts_type')),
    ]
    ])

    # response.flash = T('Welcome to web2py and GestionLibre')
    return dict(message='Prototype app', links = links)


def user(evt, args=[], vars={"_next": "gestionlibre/default/index"}):
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    current = config.current

    if evt is None:
        current.request.args = args
        current.request.vars = vars

        if args[0] == "login":
            session.form = SQLFORM.factory(
                Field("email", requires=IS_EMAIL()),
                Field("password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)),
                )

        elif args[0] == "logout":
            # erease the user object
            config.auth.user = None

            # config.auth = None
            return dict(_redirect="gestionlibre/default/index")

        elif args[0] == "register":
            session.form = SQLFORM.factory(Field("first_name", requires=IS_NOT_EMPTY()),
            Field("second_name", requires=IS_NOT_EMPTY()),
            Field("email", requires=IS_EMAIL()),
            Field("password", "password", requires = gluon.validators.CRYPT()),
            Field("retype_password", "password", requires = gluon.validators.CRYPT()),
            )
            
        else: pass

        config.html_frame.window.Bind(EVT_FORM_SUBMIT, user)

    else:
        if current.request.args[0] == "login":
            if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
                the_user = db(db.auth_user.email == session.form.vars.email).select().first()
                if the_user is not None:
                    user_data = config.auth.login_bare(session.form.vars.email, session.form.vars.password)
                    if user_data != False:
                        print "Login accepted"
                        config.html_frame.window.OnLinkClicked(current.request.vars["_next"])
                    else: print "Authentication failed"
                else: print "The user entered does not exist"
            else: print "The form did not validate"

        elif current.request.args[0] == "register":
            if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
                # password encryption web2py builtin method
                print "Form register values", session.form.vars

                # validate identical passwords
                if session.form.vars.password == session.form.vars.retype_password:
                    new_user_id = db.auth_user.insert(first_name = session.form.vars.first_name, \
                    second_name = session.form.vars.second_name, email = session.form.vars.email, \
                    password = session.form.vars.password)
                else:
                    print "The passwords do not match"
                    
                db.commit()
                
                new_user = db.auth_user[new_user_id]
                the_user = config.auth.login_bare(new_user.email, new_user.password)
                config.html_frame.window.OnLinkClicked("gestionlibre/default/index")

            elif session.form.errors:
                print "Form errors", session.form.errors
            else:
                print "The form did not validate"

        else:
            # return error message
            print "Not implemented"

    return dict(form = session.form)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()



def new_function(args = [], vars = {}):
    return dict(three_size_header = H3("A 3 size header"))
    