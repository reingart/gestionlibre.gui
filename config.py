# -*- coding: utf-8 -*-

import wx
import wx.html

from gluon import *
import gluon

SQLITE_DB_FOLDER = r""
SQLITE_DB_FILE = r'sqlite://storage.sqlite'

WX_HTML_STYLE = wx.html.HW_DEFAULT_STYLE | wx.TAB_TRAVERSAL

TEMPLATES_FOLDER = r""

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

import controllers.default, controllers.operations, controllers.crm

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

menu = MENU([
    ('Index', False, URL('gestionlibre','default','index'), []),
    ('Setup', False, None, [
        ('Populate tables', False, URL('gestionlibre','migration','importcsvdir'), []),
        ('Set options', False, URL('gestionlibre','setup','options'), []),
        ('Initialize', False, URL('gestionlibre','setup','initialize'), []),
        ]),
    ])

