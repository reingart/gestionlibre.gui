# -*- coding: utf-8 -*-

import config
URL = config.URL


# Example event handler ( Set config.MAIN_MENU
# dictionary item with "handler": "handlers.MyHandler")
def MyHandler(evt):
    print "event handler MyHandler called with event", evt.Id
    return None


def billing_button_click(evt):
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='operations',f='ria_product_billing_start'))

def current_accounts_button_click(evt):
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='crm',f='current_account_report'))

def customers_button_click(evt):
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="select", args=["customer",]))

def articles_button_click(evt):
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="articles"))

def queries_button_click(evt):
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="index"))

def movements_button_click(evt):
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='operations',f='index'))

