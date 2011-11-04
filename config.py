# -*- coding: utf-8 -*-

import sys, os

WEB2PY_FOLDER = r"/home/user/web2py"
GUI2PY_FOLDER = r"/home/user/gui2py-hg"

# import gui2py support -wxHTML FORM handling- (change the path!)
sys.path.append(GUI2PY_FOLDER)

# import web2py (change the path!)
sys.path.append(WEB2PY_FOLDER)

import wx
import wx.html

import gluon
from gluon import *

# SQLITE_DB_FOLDER = r"/home/user/web2py/applications/gestionlibre/databases/"
SQLITE_DB_FOLDER = r"/home/user/proyecto_gestion_libre/test_sqlite_db/"
SQLITE_DB_FILE = r'sqlite://storage.sqlite'

WX_HTML_STYLE = wx.html.HW_DEFAULT_STYLE | wx.TAB_TRAVERSAL

# Use the default key for the example database
HMAC_KEY = "sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a"

TEMPLATES_FOLDER = r"/home/user/gestionlibre_gui-hg/views/"
APP_NAME = "gestionlibre"

CSV_CONFIG_FILE = os.path.join(os.getcwd(), "example_db", "spanish.csv")
CSV_TABLES_ROUTE = os.path.join(os.getcwd(), "example_db", "spanish")

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

# web colors
COLORS = [
# gray scale
"000000","080808","101010","181818","202020","282828",
"303030","383838","404040","484848","505050","585858",
"606060","686868","707070","787878","808080","888888",
"909090","989898","A0A0A0","A8A8A8","B0B0B0","B8B8B8",
"C0C0C0","C8C8C8","D0D0D0","D8D8D8","E0E0E0","E8E8E8",
"F0F0F0","F8F8F8","FFFFFF",
# other
"000033","000066","000099","0000CC","0000FF",
"003300","003333","003366","003399","0033CC","0033FF",
"006600","006633","006666","006699","0066CC","0066FF",
"009900","009933","009966","009999","0099CC","0099FF",
"00CC00","00CC33","00CC66","00CC99","00CCCC","00CCFF",
"00FF00","00FF33","00FF66","00FF99","00FFCC","00FFFF",
"330000","330033","330066","330099","3300CC","3300FF",
"333300","333333","333366","333399","3333CC","3333FF",
"336600","336633","336666","336699","3366CC","3366FF",
"339900","339933","339966","339999","3399CC","3399FF",
"33CC00","33CC33","33CC66","33CC99","33CCCC","33CCFF",
"33FF00","33FF33","33FF66","33FF99","33FFCC","33FFFF",
"660000","660033","660066","660099","6600CC","6600FF",
"663300","663333","663366","663399","6633CC","6633FF",
"666600","666633","666666","666699","6666CC","6666FF",
"669900","669933","669966","669999","6699CC","6699FF",
"66CC00","66CC33","66CC66","66CC99","66CCCC","66CCFF",
"66FF00","66FF33","66FF66","66FF99","66FFCC","66FFFF",
"990000","990033","990066","990099","9900CC","9900FF",
"993300","993333","993366","993399","9933CC","9933FF",
"996600","996633","996666","996699","9966CC","9966FF",
"999900","999933","999966","999999","9999CC","9999FF",
"99CC00","99CC33","99CC66","99CC99","99CCCC","99CCFF",
"99FF00","99FF33","99FF66","99FF99","99FFCC","99FFFF",
"CC0000","CC0033","CC0066","CC0099","CC00CC","CC00FF",
"CC3300","CC3333","CC3366","CC3399","CC33CC","CC33FF",
"CC6600","CC6633","CC6666","CC6699","CC66CC","CC66FF",
"CC9900","CC9933","CC9966","CC9999","CC99CC","CC99FF",
"CCCC00","CCCC33","CCCC66","CCCC99","CCCCCC","CCCCFF",
"CCFF00","CCFF33","CCFF66","CCFF99","CCFFCC","CCFFFF",
"FF0000","FF0033","FF0066","FF0099","FF00CC","FF00FF",
"FF3300","FF3333","FF3366","FF3399","FF33CC","FF33FF",
"FF6600","FF6633","FF6666","FF6699","FF66CC","FF66FF",
"FF9900","FF9933","FF9966","FF9999","FF99CC","FF99FF",
"FFCC00","FFCC33","FFCC66","FFCC99","FFCCCC","FFCCFF",
"FFFF00","FFFF33","FFFF66","FFFF99","FFFFCC"
]
