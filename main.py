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

# load web2py app env object for GestionLibre
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
config.auth.settings.hmac_key = config.HMAC_KEY       # before define_tables()
config.auth.define_tables()                           # creates all needed tables

# crud (buggy: form submission and database transactions problems)
config.crud = gluon.tools.Crud(config.env, db=db)

# import wx auto generated classes
from gestion_libre_wx import MyHTMLFrame, MyDialog, MyFrame

# wx auto if __name ... code
def action(url):
    gui.action(url)

import controllers.default, controllers.operations, controllers.crm, \
controllers.registration, controllers.fees, \
controllers.scm, controllers.accounting, controllers.financials, \
controllers.setup, controllers.file, controllers.migration

# import handlers
import handlers

config.address = {
    "setup":{
        "index": {"action": controllers.setup.index},
        "options": {"action": controllers.setup.options},
        "option": {"action": controllers.setup.option},
        },
    "migration":{
        "import_csv_dir": {"action": controllers.migration.import_csv_dir},
        },
    "file":{
        "quit": {"action": controllers.file.quit},
        },
    "default":{
        "index": {"action": controllers.default.index},
        "new_function": {"action": controllers.default.new_function},
        "user": {"action": controllers.default.user},
        "change_layout_colors": {"action": controllers.default.change_layout_colors},
        "set_default_layout_colors": {"action": controllers.default.set_default_layout_colors},
        },
    "scm":{
        "ria_stock": {"action": controllers.scm.ria_stock},
        "change_stock": {"action": controllers.scm.change_stock},
        "stock_movement": {"action": controllers.scm.stock_movement},
        "stock_item_update": {"action": controllers.scm.stock_item_update},
        },
    "accounting":{
        "journal_entries": {"action": controllers.accounting.journal_entries},
        "journal_entry": {"action": controllers.accounting.journal_entry},
        "entry": {"action": controllers.accounting.entry},
        },
    "operations":{
        # extended format:
        # "movements_list": {"action": controllers.operations.movements_list, "window": None, "replace": False, "parent": html_frame},
        "ria_product_billing_start": {"action": controllers.operations.ria_product_billing_start},
        "ria_product_billing": {"action": controllers.operations.ria_product_billing},
        "reset_packing_slip": {"action": controllers.operations.reset_packing_slip},
        "reset_packing_slip": {"action": controllers.operations.reset_packing_slip},
        "packing_slip": {"action": controllers.operations.packing_slip},
        "update_order_allocation": {"action": controllers.operations.update_order_allocation},
        "list_order_allocations": {"action": controllers.operations.list_order_allocations},
        "order_allocation": {"action": controllers.operations.order_allocation},
        "operation_installment": {"action": controllers.operations.operation_installment},
        "index": {"action": controllers.operations.index},
        "ria_movements": {"action": controllers.operations.ria_movements},
        "ria_movements_reset": {"action": controllers.operations.ria_movements_reset},
        "ria_movements_process": {"action": controllers.operations.ria_movements_process},
        "movements_element": {"action": controllers.operations.movements_element},
        "movements_modify_element": {"action": controllers.operations.movements_modify_element},
        "movements_modify_check": {"action": controllers.operations.movements_modify_check},
        "ria_new_customer_order_reset": {"action": controllers.operations.ria_new_customer_order_reset},
        "ria_new_customer_order": {"action": controllers.operations.ria_new_customer_order},
        "new_customer_order_element": {"action": controllers.operations.new_customer_order_element},
        "new_customer_order_modify_element": {"action": controllers.operations.new_customer_order_modify_element},
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
    "registration":
        {
        "post_register_specify_firm": {"action": controllers.registration.post_register_specify_firm},
            },
    "crm":
        {
            "customer_current_account_status": {"action": controllers.crm.customer_current_account_status},
            "customer_panel": {"action": controllers.crm.customer_panel},
            "current_account_report": {"action": controllers.crm.current_account_report},
            },
    "financials":
        {
            "current_accounts_type": {"action": controllers.financials.current_accounts_type},
            "current_accounts_data": {"action": controllers.financials.current_accounts_data},
            "current_accounts_detail": {"action": controllers.financials.current_accounts_detail},
            "current_accounts_payment": {"action": controllers.financials.current_accounts_payment},
            },
    "fees":
        {
            "list_installments": {"action": controllers.fees.list_installments},
            "update_installment": {"action": controllers.fees.update_installment},
            "update_quota": {"action": controllers.fees.update_quota},
            "update_fee": {"action": controllers.fees.update_fee},
            "list_fees": {"action": controllers.fees.list_fees},
            "create_fee": {"action": controllers.fees.create_fee},
            },
}

# HTMLWindow Default Layout menu
config.menu = MENU([
    ('Index', False, URL('gestionlibre','default','index'), []),
    ('Setup', False, URL('gestionlibre','setup','index'), []),
    ])


def menu_event(evt):
    the_event = config.starting_frame.menu_events[evt.Id]
    if isinstance(the_event, basestring):
        config.html_frame.window.OnLinkClicked(the_event)
    elif callable(the_event):
        the_event(evt)
    return None

def main_menu_click(evt):
    # call action based on item widget address info
    return None

def main_menu_elements(frame, parent_menu, item_count = 0, submenu=None, is_menu_bar=False):
    menu_item = None
    try:
        menu_items = getattr(parent_menu, "menu_items")
    except AttributeError:
        parent_menu.menu_items = dict()
        menu_items = parent_menu.menu_items

    ordered_items = [(v.get("position", None), k, v) for k,v in submenu.iteritems()]
    ordered_items.sort()

    # for k, v in submenu.iteritems()
    # loop replaced by list iteration
    # it follows menu item index position order
    
    for item in ordered_items:
        k = item[1]
        v = item[2]
        pos = item[0]
        item_count += 1

        try:
            menu_items = getattr(parent_menu, "menu_items")
        except:
            parent_menu.menu_items = dict()

        if is_menu_bar == True:
            parent_menu.menu_items[k] = wx.Menu()
            parent_menu.Append(parent_menu.menu_items[k], v["label"])

            if v.has_key("submenu"):
                if len(v["submenu"]) > 0:
                    item_count = main_menu_elements(frame, parent_menu.menu_items[k], submenu=v["submenu"], item_count = item_count)

        else:
            if v.has_key("submenu"):
                if len(v["submenu"]) > 0:
                    parent_menu.menu_items[k] = wx.Menu()
                    parent_menu.AppendMenu(item_count, v["label"], parent_menu.menu_items[k])
                    item_count = main_menu_elements(frame, parent_menu.menu_items[k], submenu=v["submenu"], item_count = item_count)
                else:
                    parent_menu.menu_items[k] = v
                    menu_item = parent_menu.Append(item_count, v["label"])

                    # enable/disable
                    parent_menu.Enable(item_count, v.get("enabled", True))

            else:
                parent_menu.menu_items[k] = v
                menu_item = parent_menu.Append(item_count, v["label"])

                # enable/disable
                parent_menu.Enable(item_count, v.get("enabled", True))

            if v.get("separator", False):
                parent_menu.AppendSeparator()

        if v.has_key("action"):
            if menu_item is not None:
                if v["action"] is not None:
                    frame.Bind(wx.EVT_MENU, menu_event, menu_item)
                    frame.menu_events[menu_item.Id] = v["action"]
                    
        elif v.has_key("handler"):
            if menu_item is not None:
                if v["handler"] is not None:
                    handler_list = v["handler"].split(".")
                    the_obj = globals()[handler_list[0]]
                    for x in range(len(handler_list)):
                        if x > 0:
                            the_obj = getattr(the_obj, handler_list[x])

                    frame.Bind(wx.EVT_MENU, menu_event, menu_item)
                    frame.menu_events[menu_item.Id] = the_obj

    return item_count


if __name__ == "__main__":
    GestionLibre = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    config.starting_frame = MyFrame(None, -1, "")
    config.html_frame = MyHTMLFrame(config.starting_frame, -1, "")

    config.html_frame.window = gui.NewHtmlWindow(config.html_frame, \
    style = config.WX_HTML_STYLE)

    # html frame layout:
    html_sizer_1 = wx.BoxSizer(wx.VERTICAL)
    html_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
    html_sizer_1.Add(config.html_frame.window, 1, wx.EXPAND|wx.ALL, 5)
    html_sizer_2.Add(config.html_frame.button_6, 1, wx.ALIGN_CENTER|wx.ALL, 5)
    html_sizer_2.Add(config.html_frame.button_7, 0, wx.ALIGN_CENTER|wx.ALL, 5)
    html_sizer_1.Add(html_sizer_2, 0)
    config.html_frame.SetSize((640, 480))
    config.html_frame.SetSizer(html_sizer_1)
    config.html_frame.Layout()
    # end of html layout

    # previous and next button events
    config.html_frame.Bind(wx.EVT_BUTTON, gui.OnPreviousClick, config.html_frame.button_6)
    config.html_frame.Bind(wx.EVT_BUTTON, gui.OnNextClick, config.html_frame.button_7)

    config.starting_frame.menu_events = dict()

    GestionLibre.SetTopWindow(config.starting_frame)

    main_menu_elements(config.starting_frame, config.starting_frame.starting_menubar, \
    submenu=config.MAIN_MENU, is_menu_bar = True)

    config.starting_frame.SetMenuBar(config.starting_frame.starting_menubar)

    config.html_frame.window.OnLinkClicked("gestionlibre/default/index")

    config.starting_frame.Show()
    config.html_frame.Show()

    # gui-based user authentication
    # (incomplete)
    
    # add the html window
    GestionLibre.MainLoop()

