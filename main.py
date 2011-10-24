#!/usr/bin/python
# -*- coding: utf-8 -*-

# desktop app prototype for GestionLibre.
# Alan Etkin <spametki@gmail.com>

__author__ = "Mariano Reingart (reingart@gmail.com)"
__copyright__ = "Copyright (C) 2011 Mariano Reingart"
__license__ = "LGPL 3.0"

import sys

WEB2PY_FOLDER = r""
GUI2PY_FOLDER = r""

# import gui2py support -wxHTML FORM handling- (change the path!)
sys.path.append(GUI2PY_FOLDER)

# import web2py (change the path!)
sys.path.append(WEB2PY_FOLDER)

import gluon
from gluon import *

# from gluon.tools import *
# from gluon.dal import DAL, Field
# from gluon.sqlhtml import SQLFORM
# from gluon.sqlhtml import SQLTABLE
# from gluon.html import INPUT, FORM, TABLE, TR, TD, DIV
# from gluon.validators import IS_NOT_EMPTY, IS_EXPR, IS_NOT_IN_DB, IS_IN_SET
# from gluon.storage import Storage

# import wxPython:
import wx

# gui2py
from gui2py.form import EVT_FORM_SUBMIT


# app modules
import config
import gui

db = config.db

# import all the table definitions and options in web app's model
# model module

import applications.gestionlibre.modules.db_gestionlibre as db_gestionlibre

# define the database tables

db_gestionlibre.define_tables(db)


# import wx auto generated classes
from gestion_libre_wx import MyHTMLFrame, MyDialog, MyFrame


def custom_post_login(arg):
    contacts_per_user = len(db(db.contact_user.user_id == auth.user_id).select())
    if contacts_per_user < 1:
        redirect(URL(a="gestionlibre", c="registration", f="post_register_specify_firm"))

def custom_post_register(arg):
    redirect(URL(a="gestionlibre", c="registration", f="post_register_specify_firm"))

def on_form_submit(evt):
    "Handle submit button user action"
    global form
    print "Submitting to %s via %s with args %s"% (evt.form.action, \
    evt.form.method, evt.args)
    if form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
        print "accepted!"

        # insert the record in the table (if dbio=True this is done by web2py):
        db.person.insert(name=form.vars.name,
                         sex=form.vars.sex,
                         active=form.vars.active,
                         bio=form.vars.bio,
                        )
        # don't forget to commit, we aren't inside a web2py controller!
        db.commit()
    elif form.errors:
        print "errors", form.errors
        
    # refresh the form and table (show web2py errors)
    # table = SQLTABLE(db(db.person).select())
    # div = DIV(form, table)

    # display the updated div
    # html.SetPage(div.xml())


# wx auto if __name ... code

def action(url):
    gui.action(url)


if __name__ == "__main__":
    GestionLibre = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    config.starting_frame = MyFrame(None, -1, "")
    config.html_frame = MyHTMLFrame(config.starting_frame, -1, "")

    config.html_frame.window = gui.NewHtmlWindow(config.html_frame, \
    style = config.WX_HTML_STYLE)
    xml = gui.action("gestionlibre/default/index")
    config.html_frame.window.SetPage(xml)

    config.html_frame.window.action = action

    GestionLibre.SetTopWindow(config.starting_frame)

    config.starting_frame.Show()
    config.html_frame.Show()

    # add the html window
    GestionLibre.MainLoop()


# create the wxPython GUI application instance:
# app = wx.App(False)

# config.start_window = wx.Frame(None, title="GestiónLibre testing frame")

# create the html window
# gui.show("gestionlibre/default/index", config.start_window, style= wx.html.HW_DEFAULT_STYLE | wx.TAB_TRAVERSAL)

# connect the FORM event with the HTML browser
# html.Bind(EVT_FORM_SUBMIT, on_form_submit)

# show the main window
# config.start_window.Show()

# start the wx main-loop to interact with the user
# app.MainLoop()

