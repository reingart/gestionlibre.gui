# -*- coding: utf-8 -*-

import sys, os

WEB2PY_FOLDER = r"/home/user/web2py"
GUI2PY_FOLDER = r"/home/user/gui2py-hg"
SQLITE_DB_FOLDER = r"/home/user/web2py/applications/gestionlibre/databases/"
SQLITE_DB_FILE = r'sqlite://storage.sqlite'
HMAC_KEY = "sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a"
TEMPLATES_FOLDER = r"/home/user/gestionlibre_gui-hg/views/"
APP_NAME = "gestionlibre"

# import gui2py support -wxHTML FORM handling- (change the path!)
sys.path.append(GUI2PY_FOLDER)

# import web2py (change the path!)
sys.path.append(WEB2PY_FOLDER)

import wx
import wx.html

import gluon
from gluon import *

WX_HTML_STYLE = wx.html.HW_DEFAULT_STYLE | wx.TAB_TRAVERSAL

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
                "position": -1, "label": "", "visible": True, "enabled": False, "action": None, "submenu":{}
                }
                # replace "action"... with "handler": "module.handler" for no URL event handlers
"""


MAIN_MENU = {
            "file": {
                "position": 0, "label": "File",
                "visible": True, "enabled": True,
                "action": None,
                "submenu":{
                    "crud": {
                        "position": -1, "label": "File CRUD",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{}
                        }, # crud
                    "forms": {
                        "position": -1, "label": "Forms",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "design": {
                                "position": -1, "label": "Design",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{}
                             }, # design

                             "label": {
                                "position": -1, "label": "Label",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{}
                            }, # label
                            "various": {
                                "position": -1, "label": "Various",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{}
                            } # various
                            }, # forms submenu
                        "separator": True
                        }, # forms
                    "update": {
                        "position": -1, "label": "Update",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "price_list": {
                                "position": -1, "label": "Price list",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    "by_article": {
                                        "position": -1, "label": "By article",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    } # by_article
                                } # price_list submenu
                            }, # price_list
                            "articles": {
                                "position": -1, "label": "Articles",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    "browse": {
                                        "position": -1, "label": "Browse",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # browse
                                    "import": {
                                        "position": -1, "label": "Import",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # import
                                    "prices": {
                                        "position": -1, "label": "Prices",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # prices
                                } # articles submenu
                            }, # articles
                            "sales": {
                                "position": -1, "label": "Sales",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    "auto_apply": {
                                        "position": -1, "label": "Auto apply",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # auto_apply

                                    "verify": {
                                        "position": -1, "label": "Verify",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # verify

                                    "process_jurisdictions": {
                                        "position": -1, "label": "Process jurisdictions",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # process jurisdictions

                                    "discount_by_customer": {
                                        "position": -1, "label": "Discount by customer",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # discount by customer
                                } # sales submenu
                            }, # sales
                            "purchases": {
                                "position": -1, "label": "Purchases",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    "process_jurisdictions": {
                                        "position": -1, "label": "Process jurisdictions",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # process jurisdictions
                                } # purchases submenu
                            }, # purchases
                            "closing": {
                                "position": -1, "label": "Closing",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{} # closing submenu
                             }, # closing
                          }, # update submenu
                       }, # update
                    "transfers": {
                        "position": -1, "label": "Transfers",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "branches": {
                                "position": -1, "label": "Branches",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{}
                             }, # branches

                            "replica": {
                                "position": -1, "label": "Replica",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    "generate": {
                                        "position": -1, "label": "Generate",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # generate
                                    "send": {
                                        "position": -1, "label": "Send",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # send
                                    "receive": {
                                        "position": -1, "label": "Receive",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # receive
                                    "process": {
                                        "position": -1, "label": "Process",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{}
                                    }, # process
                                } # replica submenu
                             }, # replica
                            }, # transfers submenu
                        "separator": True
                        }, # transfers
                    "print": {
                        "position": -1, "label": "Print...",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{}
                        }, # print
                    "page_setup": {
                        "position": -1, "label": "Page setup",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{},
                        "separator": True
                        }, # page_setup
                    "options": {
                        "position": -1, "label": "Options",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "formats": {
                                "position": -1, "label": "Options",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # formats
                            "reset": {
                                "position": -1, "label": "Reset",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # reset
                            "branch": {
                                "position": -1, "label": "Branch",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # branch
                            "map": {
                                "position": -1, "label": "Map",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # map
                            "reset_password": {
                                "position": -1, "label": "Password reset",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # reset_password
                            }, # options submenu
                        }, # options
                    "parameters": {
                        "position": -1, "label": "Parameters",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "fiscal_controller": {
                                "position": -1, "label": "fiscal controller",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    "model": {
                                        "position": -1, "label": "Model",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{},
                                        }, # model
                                    "per_item_printing": {
                                        "position": -1, "label": "Per item printing",
                                        "visible": True, "enabled": False,
                                        "action": None,
                                        "submenu":{},
                                        }, # per_item_printing
                                    }, # fiscal_controller submenu
                                },  # fiscal_controller
                            "credit_card": {
                                "position": -1, "label": "Credit card",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # credit_card
                            "facilitate_collection": {
                                "position": -1, "label": "Facilitate collection",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # facilitate_collection
                            "default_salesperson": {
                                "position": -1, "label": "Default salesperson",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # default_salesperson
                            "vat_subjournal": {
                                "position": -1, "label": "VAT sub-journal",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # vat_subjournal
                            "predefine_documents": {
                                "position": -1, "label": "Predefine documents",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # predefine_documents
                            "deactivate_access_levels": {
                                "position": -1, "label": "Deactivate access levels",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # deactivate_access_levels
                            "advanced": {
                                "position": -1, "label": "Advanced",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # advanced
                            }, # parameters submenu
                        "separator": True
                        }, # parameters

                    "db_update": {
                        "position": -1, "label": "Database",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "change_location": {
                                "position": -1, "label": "Change location",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # change_location
                            "backup": {
                                "position": -1, "label": "Backup",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # backup
                            "repair": {
                                "position": -1, "label": "repair",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # repair
                            "compress": {
                                "position": -1, "label": "compress",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                }, # compress
                            }, # db_update submenu
                        "separator": True
                        }, # db_update
                    "change_user": {
                        "position": -1, "label": "Change user",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{},
                        }, # change_user
                    "change_password": {
                        "position": -1, "label": "Change password",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{},
                        }, # change_password
                    "security_policies": {
                        "position": -1, "label": "Security policies",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{},
                        "separator": True
                        }, # security_policies
                    "quit": {
                        "position": -1, "label": "Quit",
                        "visible": True, "enabled": True,
                        "action": "gestionlibre/file/quit",
                        "submenu":{},
                        }, # quit
                    } ,# file submenu
                } ,# file
            
            "sales":{
                    "position": 1, "label": "Sales",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                        "price_check":{
                                "position": -1, "label": "Price check",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # price_check

                        "create_order":{
                                "position": -1, "label": "Create order",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # create_order

                        "create_down_payment":{
                                "position": -1, "label": "Create down payment",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # create_down_payment

                        "create_invoice":{
                                "position": -1, "label": "Create invoice",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True 
                            }, # create_invoice

                        "order_allocation":{
                                "position": -1, "label": "Order allocation",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # order_allocation

                        "assign_travel":{
                                "position": -1, "label": "Assign travel",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # assign travel

                        "invoice_batch":{
                                "position": -1, "label": "Create invoice batch",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True,
                            }, # invoice batch

                        "current_accounts":{
                                "position": -1, "label": "Current accounts",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # current accounts

                        "queries":{
                                "position": -1, "label": "Queries",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # queries

                        "summary":{
                                "position": -1, "label": "Summary",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # sales summary

                        "cancel":{
                                "position": -1, "label": "Cancel",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True,
                            }, # cancel

                        "price_lists":{
                                "position": -1, "label": "Price lists",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True,
                            }, # price_lists

                        }, # sales submenu
                }, # sales

            "purchases":{
                    "position": 2, "label": "Purchases",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                        "create_invoice":{
                                "position": -1, "label": "New invoice",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # create_invoice

                        "create_expenses_invoice":{
                                "position": -1, "label": "New expenses invoice",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True,
                            }, # create_expenses_invoice

                        "create_payment":{
                                "position": -1, "label": "Create payment",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # create_payment

                        "apply_payment":{
                                "position": -1, "label": "Apply payment",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True
                            }, # apply_payment

                        "revert_application":{
                                "position": -1, "label": "Revert payment application",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True,
                            }, # revert_application

                        "current_accounts":{
                                "position": -1, "label": "Current accounts",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                                "separator": True,
                            }, # current_accounts

                        "queries":{
                                "position": -1, "label": "queries",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # queries

                        "summary":{
                                "position": -1, "label": "Summary",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # summary

                        "cancel":{
                                "position": -1, "label": "Cancel",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{},
                            }, # cancel
                        }, # purchases submenu
                }, # purchases

            "cash":{
                    "position": 3, "label": "Cash",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                        
                        "funds":{
                                "position": -1, "label": "Funds",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # funds submenu
                            }, # funds

                        "checks":{
                                "position": -1, "label": "Checks",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # checks submenu
                            }, # checks

                        "banks":{
                                "position": -1, "label": "Banks",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # banks submenu
                            }, # banks
                        }, # cash submenu
                }, # cash

            "stock":{
                    "position": 4, "label": "Stock",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                        "activate_deposit":{
                                "position": -1, "label": "Funds",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    },
                                "separator": True,
                            }, # activate_deposit
                        "queries":{
                                "position": -1, "label": "Queries",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # queries submenu
                            }, # queries

                        "summary":{
                                "position": -1, "label": "Summary",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # summary submenu
                            }, # summary


                        "articles":{
                                "position": -1, "label": "Articles",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # articles submenu
                            }, # articles


                        "structures":{
                                "position": -1, "label": "Structures",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # structures submenu
                            }, # structures


                        "formulas":{
                                "position": -1, "label": "Formulas",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # formulas submenu
                            }, # formulas

                        "production":{
                                "position": -1, "label": "Production",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # production submenu
                            }, # production
                        }, # stock submenu
                }, # stock

            "accounting":{
                    "position": 5, "label": "Accounting",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                        "activate_period":{
                                "position": -1, "label": "Activate period",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, 
                            }, # activate_period
                            
                        "entries":{
                                "position": -1, "label": "Entries",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # entries submenu
                            }, # entries

                        "accounts_plan":{
                                "position": -1, "label": "Accounts plan",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, 
                            }, # accounts_plan

                        "passages":{
                                "position": -1, "label": "Passages",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # passages submenu
                            }, # passages


                        "processes":{
                                "position": -1, "label": "Processes",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # processes submenu
                            }, # processes

                        "batch":{
                                "position": -1, "label": "Batch",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # batch submenu
                            }, # batch
                        }, # accounting submenu
                }, # accounting


            "reports":{
                    "position": 6, "label": "Reports",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                        "lists":{
                                "position": -1, "label": "Lists",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # lists submenu
                            }, # lists

                        "labels":{
                                "position": -1, "label": "Labels",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # labels submenu
                            }, # labels

                        "fiscal_controller":{
                                "position": -1, "label": "Fiscal controller",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # fiscal_controller submenu
                            }, # fiscal_controller

                        "sales":{
                                "position": -1, "label": "Sales",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # sales submenu
                            }, # sales
                            
                        "purchases":{
                                "position": -1, "label": "Purchases",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # purchases submenu
                            }, # purchases

                        "cash":{
                                "position": -1, "label": "Cash",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # cash submenu
                            }, # cash

                        "securities":{
                                "position": -1, "label": "Securities",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # securities submenu
                            }, # securities

                        "stock":{
                                "position": -1, "label": "Stock",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # stock submenu
                            }, # stock

                        "movements":{
                                "position": -1, "label": "Movements",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # movements submenu
                            }, # movements

                        "accounting":{
                                "position": -1, "label": "Accounting",
                                "visible": True, "enabled": False,
                                "action": None,
                                "submenu":{
                                    }, # accounting submenu
                            }, # accounting
                        }, # reports submenu
                }, # reports

            "windows":{
                    "position": 7, "label": "Windows",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                        }, # windows submenu
            }, # windows
            
            "help":{
                    "position": 8, "label": "Help",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{
                            "about":{
                                    "position": -1, "label": "About",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                            }, # about
                        }, # help submenu
            }, # help
            
    } # MAIN_MENU

"""
            "sales":{
                    "position": -1, "label": "Quit",
                    "visible": True, "enabled": False,
                    "action": None,
                    "submenu":{}, # sales submenu
                }, # sales

"""

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
