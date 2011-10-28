#!/usr/bin/python
# -*- coding: utf-8 -*-

# Desktop app prototype for GestionLibre.

"""
    This is a Python open source project for migration of modules
    and functions from GestionPyme and other ERP products from Sistemas
    Ágiles.

    Copyright (C) 2011 Sistemas Ágiles.

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
"""

__author__ = "Alan Etkin <spametki@gmail.com>"
__copyright__ = "Copyright (C) 2011 Sistemas Ágiles"
__license__ = "AGPLv3"

# constants and common memmory storage
import config

import sys

import gluon
import gluon.shell
import gluon.tools
from gluon import *

# import wxPython:
import wx

# gui2py
from gui2py.form import EVT_FORM_SUBMIT

# app modules
import gui

db = config.db

config.env = gluon.shell.env(config.APP_NAME, dir=config.WEB2PY_FOLDER)


# TODO: Authenticate with wx widgets.
# A series of hack imports (with shell) and bindings are needed
# for using auth and crud.

# auth (buggy: has redirection and form submission problems)
config.auth = gluon.tools.Auth(db=db, hmac_key=config.HMAC_KEY)

# import all the table definitions and options in web app's model
# model module

# custom auth_user definition is required to prevent the "auth_user not
# found" error
import applications.gestionlibre.modules.db_gestionlibre as db_gestionlibre

# define the database tables
# web2py = False forces db.define_table("auth_user"..)
db_gestionlibre.define_tables(db, web2py = False)

# define the auth tables (this goes after app tables definition)
config.auth.settings.hmac_key = 'sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a'   # before define_tables()
config.auth.define_tables()                           # creates all needed tables

# crud (buggy: form submission and database transactions problems)
config.crud = gluon.tools.Crud(config.env, db=db)

# import wx auto generated classes
from gestion_libre_wx import MyHTMLFrame, MyDialog, MyFrame

# wx auto if __name ... code
def action(url):
    gui.action(url)

import controllers.default, controllers.operations, controllers.crm

config.address = {
    "default":{
        "index": {"action": controllers.default.index},
        "new_function": {"action": controllers.default.new_function},
        "user": {"action": controllers.default.user},
        },
    "operations":{
        # extended format:
        # "movements_list": {"action": controllers.operations.movements_list, "window": None, "replace": False, "parent": html_frame},

        "movements_list": {"action": controllers.operations.movements_list},
        "movements_select": {"action": controllers.operations.movements_select},
        "movements_detail": {"action": controllers.operations.movements_detail},
        "movements_start": {"action": controllers.operations.movements_start},
        "movements_header": {"action": controllers.operations.movements_header},
        "movements_price_list": {"action": controllers.operations.movements_price_list},
        "movements_add_item": {"action": controllers.operations.movements_add_item},
        "movements_add_payment_method": {"action": controllers.operations.movements_add_payment_method},
        "movements_articles": {"action": controllers.operations.movements_articles},
        "movements_add_check": {"action": controllers.operations.movements_add_check},
        "movements_add_tax": {"action": controllers.operations.movements_add_tax},
        "movements_current_account_concept": {"action": controllers.operations.movements_current_account_concept},
        "movements_current_account_quotas": {"action": controllers.operations.movements_current_account_quotas},
        "movements_current_account_data": {"action": controllers.operations.movements_current_account_data},
        "movements_add_discount_surcharge": {"action": controllers.operations.movements_add_discount_surcharge},
        "movements_process": {"action": controllers.operations.movements_process},
        "movements_option_update_stock": {"action": controllers.operations.movements_option_update_stock},
        "movements_option_update_taxes": {"action": controllers.operations.movements_option_update_taxes},
        "movements_select_warehouse": {"action": controllers.operations.movements_select_warehouse},
        "movements_modify_item": {"action": controllers.operations.movements_modify_item},
        },
    "crm":
        {
            "customer_current_account_status": {"action": controllers.crm.customer_current_account_status},
            },
}

config.menu = MENU([
    ('Index', False, URL('gestionlibre','default','index'), []),
    ('Setup', False, None, [
        ('Populate tables', False, URL('gestionlibre','migration','importcsvdir'), []),
        ('Set options', False, URL('gestionlibre','setup','options'), []),
        ('Initialize', False, URL('gestionlibre','setup','initialize'), []),
        ]),
    ])



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

    # gui-based user authentication

    # add the html window
    GestionLibre.MainLoop()

