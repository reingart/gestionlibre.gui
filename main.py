#!/usr/bin/python
# -*- coding: utf-8 -*-

# desktop app prototype for GestionLibre.

"""
    This project is a Python open source migration of
    Sistemas Ágiles ERP software GesPyme and others.

    Copyright (C) 2011 Sistemas Ágiles

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    NOTE: Many of the app modules and functions were taken from
    the original project Visual BASIC source code.
"""

__author__ = "Alan Etkin <spametki@gmail.com>"
__copyright__ = "Copyright (C) 2011 Sistemas Ágiles"
__license__ = "AGPLv3"

import sys

WEB2PY_FOLDER = r""
GUI2PY_FOLDER = r""

# import gui2py support -wxHTML FORM handling- (change the path!)
sys.path.append(GUI2PY_FOLDER)

# import web2py (change the path!)
sys.path.append(WEB2PY_FOLDER)

import gluon
from gluon import *

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

    GestionLibre.SetTopWindow(config.starting_frame)

    config.starting_frame.Show()
    config.html_frame.Show()

    # add the html window
    GestionLibre.MainLoop()

