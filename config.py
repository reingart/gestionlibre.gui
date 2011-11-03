# -*- coding: utf-8 -*-

SQLITE_DB_FOLDER = r"/home/user/web2py/applications/gestionlibre/databases/"
SQLITE_DB_FILE = r'sqlite://storage.sqlite'

# Use the default key for the example database
HMAC_KEY = "sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a"

TEMPLATES_FOLDER = r"/home/user/gestionlibre_gui-hg/views/"
WEB2PY_FOLDER = r"/home/user/web2py"
GUI2PY_FOLDER = r"/home/user/gui2py-hg"
APP_NAME = "gestionlibre"

import sys

# import gui2py support -wxHTML FORM handling- (change the path!)
sys.path.append(GUI2PY_FOLDER)

# import web2py (change the path!)
sys.path.append(WEB2PY_FOLDER)

import wx
import wx.html

WX_HTML_STYLE = wx.html.HW_DEFAULT_STYLE | wx.TAB_TRAVERSAL

from gluon import *
import gluon

# create DAL connection (and create DB if not exists)
db = DAL(SQLITE_DB_FILE, folder=SQLITE_DB_FOLDER)

# generic web2py objects (for web server emulation)

request = current.request = gluon.globals.Request()
response = current.response = gluon.globals.Response()
session = current.session = gluon.globals.Session()
context = gluon.storage.Storage()

response._vars = gluon.storage.Storage()

# create a testing frame (wx "window"):
starting_frame = None
html_frame = None
address = None
menu = None
after_submission = dict()
env = None
crud = None
auth = None
menu = None
address = None
_auth_next = None
_auth_source = None

_this_url = -1
_urls = []

# Dictiary with menu items and event binding
"""

            "": {
                "label": "", "visible": True, "action": None, "submenu":[]
                }
                
"""
MAIN_MENU = {
            "file": {
                "label": "File",
                "visible": True,
                "action": URL(a="gestionlibre", c="file", f="quit"),
                "submenu":{
                    "crud": {
                        "label": "File CRUD",
                        "visible": True,
                        "action": None,
                        "submenu":{}
                        }, # crud
                    "forms": {
                        "label": "Forms",
                        "visible": True,
                        "action": None,
                        "submenu":{
                            "design": {
                                "label": "Design",
                                "visible": True,
                                "action": None,
                                "submenu":{}
                             }, # design
                             "label": {
                                "label": "Label",
                                "visible": True,
                                "action": None,
                                "submenu":[]
                            }, # label
                            "various": {
                                "label": "Various",
                                "visible": True,
                                "action": None,
                                "submenu":[]
                            } # various
                            }, # forms submenu
                        "separator": True
                        }, # forms
                    "update": {
                        "label": "Update",
                        "visible": True,
                        "action": None,
                        "submenu":{
                            "price_list": {
                                "label": "Price list",
                                "visible": True,
                                "action": None,
                                "submenu":{
                                    "by_article": {
                                        "label": "By article",
                                        "visible": True,
                                        "action": None,
                                        "submenu":[]
                                    } # by_article
                                } # price_list submenu
                            }, # price_list
                            "articles": {
                                "label": "Articles",
                                "visible": True,
                                "action": None,
                                "submenu":{
                                    "browse": {
                                        "label": "Browse",
                                        "visible": True,
                                        "action": None,
                                        "submenu":{}
                                    }, # browse
                                    "import": {
                                        "label": "Import",
                                        "visible": True,
                                        "action": None,
                                        "submenu":{}
                                    }, # import
                                    "prices": {
                                        "label": "Prices",
                                        "visible": True,
                                        "action": None,
                                        "submenu":{}
                                    }, # prices
                                } # articles submenu
                            }, # articles
                            "Sales": {
                                "label": "Sales",
                                "visible": True,
                                "action": None,
                                "submenu":{
                                    "auto_apply": {
                                        "label": "Auto apply",
                                        "visible": True,
                                        "action": None,
                                        "submenu":{}
                                    }, # auto_apply

                                    "verify": {
                                        "label": "Verify",
                                        "visible": True,
                                        "action": None,
                                        "submenu":{}
                                    }, # verify

                                    "process_jurisdictions": {
                                        "label": "Process jurisdictions",
                                        "visible": True,
                                        "action": None,
                                        "submenu":{}
                                    }, # process jurisdictions

                                    "discount_by_customer": {
                                        "label": "Discount by customer",
                                        "visible": True,
                                        "action": None,
                                        "submenu":{}
                                    }, # discount by customer
                                } # sales submenu
                            }, # sales
                            }, # update submenu
                        }, # update

                    "quit": {
                        "label": "Quit",
                        "visible": True,
                        "action": "gestionlibre/file/quit",
                        "submenu":{}
                        }, # crud
                        
                    } # file submenu
                } # file
                
    } # MAIN_MENU
