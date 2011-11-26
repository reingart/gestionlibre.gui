# -*- coding: utf-8 -*-

import config
import gui
URL = gui.URL

# Example event handler ( Set config.MAIN_MENU
# dictionary item with "handler": "handlers.MyHandler")
def MyHandler(evt):
    print "event handler MyHandler called with event", evt.Id
    return None


def billing_button_click(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='operations',f='ria_product_billing_start'))

def current_accounts_button_click(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='crm',f='current_account_report'))

def customers_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="select", args=["customer",]))

def articles_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="articles"))

def queries_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="index"))

def movements_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='operations',f='index'))

def user_login(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='user', args=["login",]))

def user_logout(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='user', args=["logout",]))

def user_register(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='user', args=["register",]))

def user_specify_tin(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='registration',f='post_register_specify_firm'))

def user_index(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='index'))

def user_setup(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='setup',f='index'))
