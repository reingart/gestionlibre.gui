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

import sys, os

import datetime

import gluon
import gluon.shell
import gluon.tools
from gluon import *

# import wxPython:
import wx

# gui2py
from gui2py.form import EVT_FORM_SUBMIT

# import wx auto generated classes
from gestion_libre_wx import MyHTMLFrame, MyDialog, MyFrame

# wx auto if __name ... code
def action(url):
    gui.action(url)


# move url map and main_menu definition to an
# auxiliari module

def configure_main_menu():
    config.MAIN_MENU = {
                "file": {
                    "position": 0, "label": "File",
                    "visible": True, "enabled": True,
                    "action": None,
                    "submenu":{
                        "crud": {
                            "position": 0, "label": "File CRUD",
                            "visible": True, "enabled": True,
                            "action": URL(a=config.APP_NAME, c="appadmin", f="index"),
                            "submenu":{}
                            }, # crud
                        "forms": {
                            "position": 1, "label": "Forms",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "design": {
                                    "position": 0, "label": "Design",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                }, # design

                                "label": {
                                    "position": 1, "label": "Label",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                }, # label
                                "various": {
                                    "position": 2, "label": "Various",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                } # various
                                }, # forms submenu
                            "separator": True
                            }, # forms
                        "update": {
                            "position": 2, "label": "Update",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "price_list": {
                                    "position": 0, "label": "Price list",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "by_article": {
                                            "position": -1, "label": "By article",
                                            "visible": True, "enabled": True,
                                            "action": URL(a=config.APP_NAME, c="appadmin", f="select", args=["price", ]),
                                            "submenu":{}
                                        } # by_article
                                    } # price_list submenu
                                }, # price_list
                                "articles": {
                                    "position": 1, "label": "Articles",
                                    "visible": True, "enabled": True,
                                    "action": None,
                                    "submenu":{
                                        "browse": {
                                            "position": -1, "label": "Browse",
                                            "visible": True, "enabled": True,
                                            "action": URL(a=config.APP_NAME, c="operations", f="articles"),
                                            "submenu":{}
                                        }, # browse
                                        "import": {
                                            "position": 0, "label": "Import",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # import
                                        "prices": {
                                            "position": 1, "label": "Prices",
                                            "visible": True, "enabled": True,
                                            "action": URL(a=config.APP_NAME, c="appadmin", f="select", args=["price",]),
                                            "submenu":{}
                                        }, # prices
                                    } # articles submenu
                                }, # articles
                                "sales": {
                                    "position": 2, "label": "Sales",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "auto_apply": {
                                            "position": 0, "label": "Auto apply",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # auto_apply

                                        "verify": {
                                            "position": 1, "label": "Verify",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # verify

                                        "process_jurisdictions": {
                                            "position": 2, "label": "Process jurisdictions",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # process jurisdictions

                                        "discount_by_customer": {
                                            "position": 3, "label": "Discount by customer",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # discount by customer
                                    } # sales submenu
                                }, # sales
                                "purchases": {
                                    "position": 3, "label": "Purchases",
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
                                    "position": 4, "label": "Closing",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{} # closing submenu
                                }, # closing
                            }, # update submenu
                        }, # update
                        "transfers": {
                            "position": 3, "label": "Transfers",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "branches": {
                                    "position": 0, "label": "Branches",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                }, # branches

                                "replica": {
                                    "position": 1, "label": "Replica",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "generate": {
                                            "position": 0, "label": "Generate",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # generate
                                        "send": {
                                            "position": 1, "label": "Send",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # send
                                        "receive": {
                                            "position": 2, "label": "Receive",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # receive
                                        "process": {
                                            "position": 3, "label": "Process",
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
                            "position": 4, "label": "Print...",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{}
                            }, # print
                        "page_setup": {
                            "position": 5, "label": "Page setup",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{},
                            "separator": True
                            }, # page_setup
                        "options": {
                            "position": 6, "label": "Options",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "formats": {
                                    "position": 0, "label": "Options",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c="setup", f="index"),
                                    "submenu":{},
                                    }, # formats
                                "reset": {
                                    "position": 1, "label": "Reset",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # reset
                                "branch": {
                                    "position": 2, "label": "Branch",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # branch
                                "map": {
                                    "position": 3, "label": "Map",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # map
                                "reset_password": {
                                    "position": 4, "label": "Password reset",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # reset_password
                                }, # options submenu
                            }, # options
                        "parameters": {
                            "position": 7, "label": "Parameters",
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
                            "position": 8, "label": "Database",
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
                            "position": 9, "label": "Change user",
                            "visible": True, "enabled": True,
                            "action": URL(a=config.APP_NAME, c="default", f="user", args=["login",]),
                            "submenu":{},
                            }, # change_user
                        "change_password": {
                            "position": 10, "label": "Change password",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{},
                            }, # change_password
                        "security_policies": {
                            "position": 11, "label": "Security policies",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{},
                            "separator": True
                            }, # security_policies
                        "quit": {
                            "position": 12, "label": "Quit",
                            "visible": True, "enabled": True,
                            "action": "%s/file/quit" % config.APP_NAME,
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='crm',f='customer_panel'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c="operations", f="movements_start"),
                                    "submenu":{},
                                    "separator": True
                                }, # create_invoice

                            "order_allocation":{
                                    "position": -1, "label": "Order allocation",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='operations',f='order_allocation'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='financials',f='current_accounts_type'),
                                    "submenu":{},
                                }, # current accounts

                            "queries":{
                                    "position": -1, "label": "Queries",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='index'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["price_list",]),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='operations',f='movements_start'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='financials',f='current_accounts_type'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='index'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["fund",]),
                                    "submenu":{
                                        }, # funds submenu
                                }, # funds

                            "checks":{
                                    "position": -1, "label": "Checks",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["bank_check",]),
                                    "submenu":{
                                        }, # checks submenu
                                }, # checks

                            "banks":{
                                    "position": -1, "label": "Banks",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["bank",]),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["stock",]),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='scm',f='ria_stock'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='accounting',f='journal_entries'),
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
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='operations',f='movements_list'),
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
                        "visible": True, "enabled": True,
                        "action": None,
                        "submenu":{
                                "wiki":{
                                        "position": -1, "label": "Wiki",
                                        "visible": True, "enabled": True,
                                        "action": "http://code.google.com/p/gestionlibre/w/list",
                                        "submenu":{},
                                }, # about
                                "about":{
                                        "position": -1, "label": "About",
                                        "visible": True, "enabled": True,
                                        "action": "http://code.google.com/p/gestionlibre/",
                                        "submenu":{},
                                }, # about
                            }, # help submenu
                }, # help

        } # MAIN_MENU



# bind actions to functions
def configure_addresses():
    
    import controllers.default, controllers.operations, controllers.crm, \
    controllers.registration, controllers.fees, \
    controllers.scm, controllers.accounting, controllers.financials, \
    controllers.setup, controllers.file, controllers.migration, \
    controllers.appadmin, controllers.output

    config.address = {
        "appadmin": {
            "index": {"action": controllers.appadmin.index},
            "select": {"action": controllers.appadmin.select},
            "read": {"action": controllers.appadmin.read},
            "update": {"action": controllers.appadmin.update},
            "create": {"action": controllers.appadmin.create},
            },
        "setup":{
            "index": {"action": controllers.setup.index},
            "options": {"action": controllers.setup.options},
            "option": {"action": controllers.setup.option},
            "set_language": {"action": controllers.setup.set_language},
            },
        "migration":{
            "import_csv_dir": {"action": controllers.migration.import_csv_dir},
            },
        "file":{
            "quit": {"action": controllers.file.quit},
            },
        "output":{
            "operation": {"action": controllers.output.operation},
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
            "articles": {"action": controllers.operations.articles},
            "articles_list": {"action": controllers.operations.articles_list},
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


# end of bind actions


# HTMLWindow Default Layout menu
config.menu = MENU([
    ('Index', False, URL(config.APP_NAME,'default','index'), []),
    ('Setup', False, URL(config.APP_NAME,'setup','index'), []),
    ])


def menu_event(evt):

    # check if html_frame was closed (throws wx._core.PyDeadObjectError)

    the_event = config.starting_frame.menu_events[evt.Id]
    if isinstance(the_event, basestring):
        try:
            is_active = config.html_frame.IsActive()
        except wx._core.PyDeadObjectError:
            # html window closed
            # reinitialize it
            gui.start_html_frame(config.starting_frame, the_event)

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


        if v.get("visible", False):
            
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
    # load web2py app env object for GestionLibre

    config.env = gluon.shell.env(config.WEB2PY_APP_NAME, dir=config.WEB2PY_FOLDER)

    config.request = config.current.response = config.env["request"]
    config.response = config.current.response = config.env["response"]
    config.response._vars = gluon.storage.Storage()
    config.session = config.current.session = config.env["session"]
    config.context = gluon.storage.Storage()

    # set translation options
    # language configuration values are forced
    # because of the non web2py execution environment

    T = config.env["T"]
    T.folder = config.WEB2PY_APP_FOLDER

    # test if language file exists or create it (except for default "en" value)
    if not (config.LANGUAGE in (None, "", "en")):
        language_file_path = os.path.join(config.WEB2PY_FOLDER, "applications", \
        config.WEB2PY_APP_NAME, "languages", "%s.py" % config.LANGUAGE)

        """
        if not ("%s.py" % config.LANGUAGE) in (os.listdir(os.path.join(config.WEB2PY_APP_FOLDER, "languages"))):
            if config.LANGUAGE != "en":
                # create file
                with open(config.env["T"].language_file, "w") as language_file:
                    language_file.write("# -*- coding: utf-8 -*-")
                    language_file.write("\n")

                print "Language file is", config.env["T"].language_file

        """

        # config.env["T"].set_current_languages([config.LANGUAGE,])
        T.language_file = language_file_path
        T.accepted_language = config.LANGUAGE
        T.http_accept_language = [config.LANGUAGE,]
        T.requested_languages = [config.LANGUAGE,]

        # force t dictionary load (otherwise translator would overwrite
        # the language file)
        T.t = gluon.languages.read_dict(T.language_file)

    # create DAL connection (and create DB if it does not exists)
    config.db = DAL(config.SQLITE_DB_FILE, folder=config.SQLITE_DB_FOLDER)
    db = config.db

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

    db_gestionlibre.define_tables(db, config.auth, config.env, web2py = False)

    # define the auth tables (this goes after app tables definition)
    config.auth.settings.hmac_key = config.HMAC_KEY       # before define_tables()
    config.auth.define_tables()                           # creates all needed tables

    # crud (buggy: form submission and database transactions problems)
    config.crud = gluon.tools.Crud(config.env, db=db)


    GestionLibre = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    config.starting_frame = MyFrame(None, -1, "")
    config.starting_frame.SetSize((640, 360))

    # app modules
    import gui
    import handlers

    # Main window button events
    config.starting_frame.Bind(wx.EVT_BUTTON, handlers.billing_button_click, config.starting_frame.button_1)
    config.starting_frame.Bind(wx.EVT_BUTTON, handlers.current_accounts_button_click, config.starting_frame.button_2)
    config.starting_frame.Bind(wx.EVT_BUTTON, handlers.customers_button_click, config.starting_frame.button_3)
    config.starting_frame.Bind(wx.EVT_BUTTON, handlers.articles_button_click, config.starting_frame.button_4)
    config.starting_frame.Bind(wx.EVT_BUTTON, handlers.queries_button_click, config.starting_frame.button_5)
    config.starting_frame.Bind(wx.EVT_BUTTON, handlers.movements_button_click, config.starting_frame.button_8)
    config.starting_frame.menu_events = dict()

    # populate main menu
    configure_main_menu()

    GestionLibre.SetTopWindow(config.starting_frame)

    main_menu_elements(config.starting_frame, config.starting_frame.starting_menubar, \
    submenu=config.MAIN_MENU, is_menu_bar = True)

    config.starting_frame.SetMenuBar(config.starting_frame.starting_menubar)
    config.starting_frame.SetStatusText("")

    config.starting_frame.Show()

    # bind web2py like actions to module functions
    configure_addresses()

    gui.start_html_frame(config.starting_frame)

    # Gui-based user authentication
    # (incomplete)
    
    # Add the html window

    GestionLibre.MainLoop()

