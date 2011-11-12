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
    
    Project's index page
    """
    # Feedback for action redirections
    
    message = config.session.get("message", None)
    if config.session.message is None:
        message = "Desktop App"
    else:
        config.session.message = None

    return dict(message=message)


def change_layout_colors(evt, args=[], vars={}):
    if session.get("layout_colors", None) is None:
        session.layout_colors = ["#" + color for color in config.COLORS]
    session.form = SQLFORM.factory(Field("background"), Field("foreground"), Field("links"), Field("random", "boolean"))
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.random == True:
                import random
                session.layout_colors_background = "#" + str(random.choice(config.COLORS))
                session.layout_colors_foreground = "#" + str(random.choice(config.COLORS))
                session.layout_colors_links = "#" + str(random.choice(config.COLORS))
            else:
                session.layout_colors_background = session.form.vars.background
                session.layout_colors_foreground = session.form.vars.foreground
                session.layout_colors_links = session.form.vars.links

            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="default", f="change_layout_colors"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, change_layout_colors)
    
    return dict(form = session.form)

def set_default_layout_colors(evt, args=[], vars={}):

    if config.auth.user is not None:
        user_id = config.auth.user_id
        fg_option = db(db.option.name == "user_%s_layout_fgcolor" % user_id).select().first()
        bg_option = db(db.option.name == "user_%s_layout_bgcolor" % user_id).select().first()
        lnk_option = db(db.option.name == "user_%s_layout_lnkcolor" % user_id).select().first()

        if fg_option is None:
            fg_option_id = db.option.insert(name="user_%s_layout_fgcolor" % user_id, value=config.session.layout_colors_foreground)
        else:
            fg_option.update_record(value=config.session.layout_colors_foreground)

        if bg_option is None:
            db.option.insert(name="user_%s_layout_bgcolor" % user_id, value=config.session.layout_colors_background)
        else:
            bg_option.update_record(value=config.session.layout_colors_background)
            
        if lnk_option is None:
            db.option.insert(name="user_%s_layout_lnkcolor" % user_id, value=config.session.layout_colors_links)
        else:
            lnk_option.update_record(value=config.session.layout_colors_links)


        db.commit()

    return dict(_redirect=config._urls[config._this_url])


def user(evt, args=[], vars={"_next": URL(a=config.APP_NAME, c="default", f="index")}):
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

            # erease customization
            config.session.layout_colors_background \
            = config.session.layout_colors_foreground \
            = config.session.layout_colors_links = None

            # config.auth = None
            return dict(_redirect=URL(a=config.APP_NAME, c="default", f="index"))

        elif args[0] == "register":
            session.form = SQLFORM.factory(Field("first_name", requires=IS_NOT_EMPTY()),
            Field("last_name", requires=IS_NOT_EMPTY()),
            Field("email", requires=IS_EMAIL()),
            Field("password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)),
            Field("retype_password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)),
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
                # validate identical passwords
                if session.form.vars.password == session.form.vars.retype_password:
                    new_user_id = db.auth_user.insert(first_name = session.form.vars.first_name, \
                    last_name = session.form.vars.last_name, email = session.form.vars.email, \
                    password = session.form.vars.password)
                else:
                    print "The passwords do not match"
                    
                db.commit()
                
                new_user = db.auth_user[new_user_id]
                the_user = config.auth.login_bare(new_user.email, new_user.password)
                config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="default", f="index"))

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
    