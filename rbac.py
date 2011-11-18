# -*- coding: utf-8 -*-

"""
    Auxiliar module for RBAC like Access control
    with GestiónLibre
"""

# import wx
# import wx.html

import os

# from gluon import *
# import gluon

import config
db = config.db
session = config.session
response = config.response
auth = config.auth
address = config.address

from url import get_function, create_address

T = config.env["T"]

# import gui

# Look trough a list of web2py role based conditions
# and return True/False (middle actions like
# user interaction widgets can be added)

# A dictionary with function names and messages
_messages = {
    "my_access_control" : T("This action requires authenticated users"),
}

# rbac functions return boolean values. The return value
# is tested against authentication and access control
# queries

def my_access_control(**kwargs):
    if auth.is_logged_in():
        return True
    else:
        print T("This action requires authenticated users")
        return False
