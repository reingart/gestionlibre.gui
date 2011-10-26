# -*- coding: utf-8 -*- 
from gluon import *
import gluon


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

    links = UL(*[LI(a) for a in [A("GestionLibre", _href="http://code.google.com/p/gestionlibre/"),
    A(B("Customer control panel (requires registration and login)"), _href=URL(a="gestionlibre", c='crm',f='customer_panel')),
    A(B("Movements panel"), _href=URL(a="gestionlibre", c='operations',f='index')),
    A(B("RIA Stock"), _href=URL(a="gestionlibre", c='scm',f='ria_stock')),
    A(B("Journal entries"), _href=URL(a="gestionlibre", c='accounting',f='journal_entries')),
    A(B("Order allocation"), _href=URL(a="gestionlibre", c='operations',f='order_allocation')),
    A(B("Order allocation list"), _href=URL(a="gestionlibre", c='operations',f='list_order_allocations')),
    A(B("Packing slip"), _href=URL(a="gestionlibre", c='operations',f='packing_slip')),
    A(B("RIA Receipt"), _href=URL(a="gestionlibre", c='operations',f='ria_receipt')),
    A(B("RIA Product billing"), _href=URL(a="gestionlibre", c='operations',f='ria_product_billing')),
    A(B("Current account report"), _href=URL(a="gestionlibre", c='crm',f='current_account_report')),
    A(B("Movements list"), _href=URL(a="gestionlibre", c='operations',f='movements_list')),
    A(B("New operation (movements form)"), _href=URL(a="gestionlibre", c='operations',f='movements_start')),
    A(B("Current accounts payments"), _href=URL(a="gestionlibre", c='financials',f='current_accounts_type')),
    A(B("Administrative interface"), _href=URL('admin','default','index'))] ])

    # response.flash = T('Welcome to web2py and GestionLibre')
    return dict(message='Prototype app', links = links)


def user():
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
    return dict(form=auth())


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
    