# -*- coding: utf-8 -*-

import gluon
from gluon import *
import datetime
import config

db = config.db
session = config.session
request = config.request

import applications.gestionlibre.modules.operations as operations
import applications.gestionlibre.modules.crm as crm

from gui2py.form import EVT_FORM_SUBMIT

def index(): return dict(message="hello from fees.py")

def list_fees(evt, args=[], vars={}):
    return dict(fees = SQLTABLE(db(db.fee).select(), \
    columns = ["fee.fee_id", "fee.code", "fee.description", \
    "fee.due_date", "fee.document_id", "fee.starting", "fee.ending"], \
    headers = {"fee.fee_id": "Edit", "fee.code": "Code", \
    "fee.description": "Description", "fee.due_date": "Due date", \
    "fee.document_id": "Document", "fee.starting": "Starting", \
    "fee.ending": "Ending"}, \
    linkto=URL(a="gestionlibre", c="fees", f="update_fee")))
    
def update_fee(evt, args=[], vars={}):

    if len(args) > 1:
        session.fee_id = args[1]
    session.form = SQLFORM(db.fee, session.fee_id)

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.fee[session.fee_id].update_record(**session.form.vars)
            db.commit()
            print "Fee updated"
            return config.html_frame.window.OnLinkClicked(URL(a="gestionlibre", c="fees", f="list_fees"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update_fee)

    return dict(form = session.form)
    
def create_fee(evt, args=[], vars={}):
    session.form = SQLFORM(db.fee)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.fee.insert(**session.form.vars)
            db.commit()
            print "Fee updated"
            return config.html_frame.window.OnLinkClicked(URL(a="gestionlibre", c="fees", f="list_fees"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, create_fee)
    return dict(form = session.form)

def list_installments(evt, args=[], vars={}):
    operation = db.operation[session.operation_id]
    
    query = (db.installment.customer_id == operation.customer_id)
    query |= (db.installment.subcustomer_id == operation.subcustomer_id)
    query |= (db.installment.supplier_id == operation.supplier_id)

    preset = db(query)
    
    return dict(installments = SQLTABLE(preset.select(), \
    columns = ["installment.installment_id","installment.customer_id",\
    "installment.subcustomer_id","installment.supplier_id", \
    "installment.fee_id", "installment.quotas"], \
    headers = {"installment.installment_id": "Edit", \
    "installment.customer_id": "Customer",\
    "installment.subcustomer_id": "Subcustomer", \
    "installment.supplier_id": "Supplier", \
    "installment.fee_id": "Fee", "installment.quotas": "Quotas"}, \
    linkto=URL(a="gestionlibre", c="fees", f="update_installment")))


def update_installment(evt, args=[], vars={}):
    if len(args) > 1:
        session.installment_id = int(args[1])
    session.form = SQLFORM(db.installment, session.installment_id)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.installment[session.installment_id].update_record(**session.form.vars)
            db.commit()
            print "Installment updated"
            return config.html_frame.window.OnLinkClicked(URL(a="gestionlibre", c="fees", f="update_installment"))
            
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update_installment)

    quotas = SQLTABLE(db(\
    db.quota.installment_id == session.installment_id).select(), \
    columns = ["quota.quota_id","quota.number",\
    "quota.due_date", \
    "quota.fee_id", "quota.amount"], \
    headers = {"quota.quota_id": "Edit","quota.number": "Number",\
    "quota.due_date": "Due date", \
    "quota.fee_id": "Fee", "quota.amount": "Quota"}, \
    linkto=URL(a="gestionlibre", c="fees", f="update_quota.html"))

    return dict(form = session.form, quotas = quotas)


def list_quotas():
    return dict(quotas = SQLTABLE(db(\
    db.quota.installment_id == session.installment_id).select(), \
    columns = ["quota.quota_id","quota.number",\
    "quota.due_date", \
    "quota.fee_id", "quota.amount"], \
    headers = {"quota.quota_id": "Edit","quota.number": "Number",\
    "quota.due_date": "Due date", \
    "quota.fee_id": "Fee", "quota.amount": "Quota"}, \
    linkto=URL(a="gestionlibre", c="fees", f="update_quota.html")))
    
def update_quota(evt, args=[], vars={}):
    if len(args) > 1:
        session.quota_id = args[1]
    session.form = SQLFORM(db.quota, session.quota_id)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.quota[session.quota_id].update_record(**session.form.vars)
            db.commit()
            print "Quota updated"
            return config.html_frame.window.OnLinkClicked(URL(a="gestionlibre", c="fees", f="update_installment"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update_quota)
    return dict(form = session.form)
