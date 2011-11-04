# -*- coding: utf-8 -*-

""" Setup for development db """

from gluon import *
import gluon

import gluon.validators

from gui2py.form import EVT_FORM_SUBMIT

import config
db = config.db
session = config.session

def index(evt, args=[], vars={}):

    # get or create admin users group
    try:
        session.admin_group_id = db(db.auth_group.role == "admin").select().first().id
    except (AttributeError, KeyError, ValueError):
        session.admin_group_id = None
    
    if session.get("admin_group_id", None) is None:
        session.admin_group_id = db.auth_group.insert(role="admin")
        db.commit()
        print "Admin user group created"

    # create an admin user creation form
    session.form = SQLFORM.factory(Field("first_name", requires=IS_NOT_EMPTY()), Field("second_name", requires=IS_NOT_EMPTY()), Field("email", requires=IS_EMAIL()), Field("password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)), Field("retype_password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)))

    # look for administrative user
    try:
        session.admin_user_id = db(db.auth_membership.group_id == session.admin_group_id).select().first().id
    except (AttributeError, KeyError, ValueError):
        session.admin_user_id = None

    # if no admin user prompt (form) user and password for creation
    if session.admin_user_id is None:
        first_run_form = session.form
    else:
        first_run_form = None

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.password == session.form.vars.retype_password:
                session.admin_user_id = db.auth_user.insert(first_name = session.form.vars.first_name, \
                second_name = session.form.vars.second_name, email = session.form.vars.email, \
                password = session.form.vars.password)

                # assign admin membership
                db.auth_membership.insert(user_id = session.admin_user_id, group_id = session.admin_group_id)

                db.commit()
                
                print "User %s created with password %s" % (session.admin_user_id, session.form.vars.password)
                print "You should configure a firm tax id to use ordering forms"
                
                return config.html_frame.window.OnLinkClicked(URL(a="gestionlibre", c="setup", f="index"))
            else:
                print "The passwords do not match"
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, index)

    actions = [
        A("Options", _href=URL(a="gestionlibre", c="setup", f="options")), A("Load tables from CSV", _href=URL(a="gestionlibre", c="migration", f="import_csv_dir"))
        ]
    
    return dict(actions = actions, first_run_form = first_run_form, vars = vars)


def setup(evt, args=[], vars={}):
    return dict()


def options(evt, args=[], vars={}):
    the_options = SQLTABLE(db(db.option).select(), linkto=URL(a="gestionlibre", c="setup", f="option"))
    return dict(options = the_options)


def option(evt, args=[], vars={}):
    if len(args) > 0:
        session.the_option_id = args[1]
    else:
        if evt is None:
            session.the_option_id = None
        
    if session.get("the_option_id", None) is not None:
        session.form = SQLFORM(db.option, session.the_option_id)
    else:
        session.form = SQLFORM(db.option)

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.get("the_option_id", None) is None:
                session.the_option_id = db.option.insert(**session.form.vars)
            else:
                session.the_option_id = db.option[session.the_option_id].update_record(**session.form.vars)
            db.commit()
            print "Form accepted"
            return config.html_frame.window.OnLinkClicked(URL(a="gestionlibre", c="setup", f="options"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, option)

    return dict(form = session.form)


def initialize():
    message = ""
    
    # general dictionary for db initial setup
    # Incomplete
    
    # db data input design:
    # records: {
    #    "table_x": [ { "field_a": value, "field_b": value, ... }, ... { } ]
    # }
    
    records = dict()
    
    # for each tablename in records
    #     for each dictionary object obj in records["tablename"]:
    #         insert unpacked obj in tablename
    
    message="Done"
    return dict(message=message, records = len(records))
