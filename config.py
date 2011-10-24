# -*- coding: utf-8 -*-

import wx
import wx.html

from gluon import *
import gluon

SQLITE_DB_FOLDER = r""
SQLITE_DB_FILE = r'sqlite://storage.sqlite'

WX_HTML_STYLE = wx.html.HW_DEFAULT_STYLE | wx.TAB_TRAVERSAL

# create DAL connection (and create DB if not exists)
db = DAL(SQLITE_DB_FILE, folder=SQLITE_DB_FOLDER)

# generic web2py objects (for web server emulation)

request = current.request = gluon.globals.Request()
response = current.response = gluon.globals.Response()
session = current.session = gluon.globals.Session()

# address = {"operations": { "f": {"action": controllers.operations.f, "window": None } } }
# action: the route to the function: i.e.: controllers.default.index
# replace: close current window on new call

# create a testing frame (wx "window"):
starting_frame = None
html_frame = None
address = None
menu = None

import controllers.default, controllers.operations

address = {
    "default":{
        "index": {"action": controllers.default.index},
        "new_function": {"action": controllers.default.new_function},
        },
    "operations":{
        # extended format:
        # "movements_list": {"action": controllers.operations.movements_list, "window": None, "replace": False, "parent": html_frame},
        
        "movements_list": {"action": controllers.operations.movements_list},
        "movements_select": {"action": controllers.operations.movements_select},
        "movements_detail": {"action": controllers.operations.movements_detail},
        "movements_start": {"action": controllers.operations.movements_start},
        "movements_header": {"action": controllers.operations.movements_header},
        },
}

"""
# TODO: AUTO REFERENCED HTML WINDOW EVENTS BY ADDRESS
event = {
    address, evt type/id, run function x
    }

"""


menu = MENU([
    ('Index', False, URL('gestionlibre','default','index'), []),
    ('Setup', False, None, [
        ('Populate tables', False, URL('gestionlibre','migration','importcsvdir'), []),
        ('Set options', False, URL('gestionlibre','setup','options'), []),
        ('Initialize', False, URL('gestionlibre','setup','initialize'), []),
        ]),
    ])

