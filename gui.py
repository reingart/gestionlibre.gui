# -*- coding: utf-8 -*-

import wx
import wx.html

from gluon import *
import gluon
import config

import os, sys

import urllib

db = config.db
session = config.session
response = config.response
auth = config.auth

from url import get_function, create_address
address = config.address
import gluon.template

from gestion_libre_wx import MyHTMLFrame, MyDialog, MyFrame, MyLoginDialog

# from AuiNotebook_Demo_2 import TabPanel, AUIManager, AUINotebook, DemoFrame

T = config.env["T"]

""" IMPORTANT:
replace the normal response, session, ... in web2py views with

config.session, config.response, config.session, ...
"""

# This output redirection code was taken from
# Mouse vs. Python blog (Mike Driscoll)
# The source Licence is L-GPL

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


class RBAC(object):
    """ Object to handle application wide control access """
    def __init__(self, db, auth, request, session, frame, htmlwindow=None, times = 3):
        self.frame = frame
        self.db = db
        self.auth = auth
        self.request = request
        self.session = session
        self.times = times
        self.htmlwindow = htmlwindow
        self.email = None
        self.password = None
        
        # load rbac module functions
        # for access control tests

        # Access control functions
        self.acf = dict(rbac = dict())
        import rbac

        for f in dir(rbac):
            if not f.startswith("_"):
                tmp_object = getattr(rbac, f)
                if callable(tmp_object):
                    if tmp_object.__module__ == "rbac":
                        # add function to the module
                        # dict
                        try:
                            message = rbac._messages[f]
                            if message != None:
                                message = T(message)

                        except KeyError:
                            message = None

                        self.acf["rbac"][f] = dict(function = getattr(rbac, f), message = message)

    def __call__(self, requires, times = None):
        # requires set must be
        # collected by the calling object

        # map requires to a dict of name, True/False values

        self.email = self.password = None

        if times == None:
            times = self.times

        requires_rights = dict()
        for require in requires:
            requires_rights[require] = False

        rights = False
        
        while rights == False:
            if not False in requires_rights.values():
                rights = True
                return (rights, T("No errors"))

            else:
                for require in requires:
                    if requires_rights[require] != True:
                        # module, function as strings
                        name_list = require.split(".")
                        
                        condition = self.acf[name_list[0]][name_list[1]]["function"]( \
                        db = self.db, auth = self.auth, \
                        session = self.session, request = self.request)
                        
                        message = self.acf[name_list[0]][name_list[1]]["message"]

                        if condition is False:
                            authenticated = False
                            
                            rbac_window = MyLoginDialog(self.frame)
                            rbac_window.label_1.SetLabel(str(T(message)))
                            rbac_window.label_3.SetLabel(str(T("email")))
                            rbac_window.label_2.SetLabel(str(T("password")))

                            for x in range(self.times):
                                result = rbac_window.ShowModal()
                                
                                self.email = rbac_window.text_ctrl_1.GetValue()
                                self.password = rbac_window.text_ctrl_2.GetValue()
                                
                                if (result == wx.ID_OK) and (self.validate_user(self.email, self.password)):
                                    authenticated = True
                                    break
                                else:
                                    rbac_window.label_1.SetLabel(str(T("User or password did not validate")))

                            # if authentication failed or window is cancelled
                            #     exit with error message and return False

                            if authenticated == False:
                                return (False, "Authentication failed")
                            else:
                                # else set requirement name as True
                                requires_rights[require] = True
                        else:
                            requires_rights[require] = True

        #     if rights is True
        #         return True with message

        if rights == True:
            return (rights, "No errors")
        else:
            # return False with message
            return (rights, "Errors on authentication")


    def validate_user(self, email, password):
        # compare ciphered password text for the given user email
        crypt = gluon.validators.CRYPT(key=auth.settings.hmac_key)
        the_user = db(db.auth_user.email == email).select().first()
        
        # if data is correct, authenticate user
        # if data is not correct, return error/False
        if the_user is None:
            return False
        else:
            # call the web2py password service
            processed_password = crypt(password)[0]
            if config.auth.login_bare(email, processed_password) != False:
                return True

        return False

# method overriding for handling click on links
class NewHtmlWindow(wx.html.HtmlWindow):
    def OnLinkClicked(self, link, kind=None):
        # TODO: special gui function call
        # APP_NAME/wx/module.function
        # (arguments can be stored at session object
        # but not passed to the handler)
        # controller "wx" must be reserved
        # (not used as a common controller module)
        # For both basestring and link object URLs
        # test if application is config.APP_NAME
        # and controller is "wx". Then call function
        # (replace module.function with arg1, arg2, ...)

        # TODO: support for multiple encodings in HTMLWindow input
        # by default utf-8

        # TODO: move this command to an application specific
        # class or function

        config.html_frame.SetActionTools([])

        if isinstance(link, basestring):
            if (link.startswith("/%s" % config.APP_NAME) or \
            link.startswith(config.APP_NAME)):
                xml = action(link)
                if xml is not None:
                    config.html_frame.window.SetPage(unicode(xml, "utf-8"))
            else:
                # non application url
                config.html_frame.window.LoadPage(link)

            set_url(link, kind=kind)

        else:
            if not (link.Href.startswith("/%s" % config.APP_NAME) or \
            link.Href.startswith(config.APP_NAME)):
                # web source
                wx.html.HtmlWindow.OnLinkClicked(self, link)
            else:
                # application action address
                xml = action(link.Href)
                if xml is not None:
                    config.html_frame.window.SetPage(unicode(xml, "utf-8"))

            set_url(link.Href, kind=kind)


def start_html_frame(starting_frame, url=None):
    config.html_frame = MyHTMLFrame(starting_frame, -1, "")
    config.html_frame.window = NewHtmlWindow(config.html_frame, \
    style = config.WX_HTML_STYLE)

    # html frame layout:
    html_sizer_1 = wx.BoxSizer(wx.VERTICAL)
    html_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
    html_sizer_1.Add(config.html_frame.window, 1, wx.EXPAND|wx.ALL, 5)
    html_sizer_2.Add(config.html_frame.button_6, -1, wx.ALIGN_CENTER|wx.ALL, 5)
    html_sizer_2.Add(config.html_frame.button_9, -1, wx.ALIGN_CENTER|wx.ALL, 5)
    html_sizer_2.Add(config.html_frame.button_7, -1, wx.ALIGN_CENTER|wx.ALL, 5)
    html_sizer_1.Add(html_sizer_2, 0)
    config.html_frame.SetSize((640, 480))
    config.html_frame.SetSizer(html_sizer_1)
    config.html_frame.Layout()
    # end of html layout

    # Previous and next button events
    config.html_frame.Bind(wx.EVT_BUTTON, OnPreviousClick, config.html_frame.button_6)
    config.html_frame.Bind(wx.EVT_BUTTON, OnNextClick, config.html_frame.button_7)
    config.html_frame.Bind(wx.EVT_BUTTON, OnHomeClick, config.html_frame.button_9)

    if url is None:
        config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="default", f="index"))
    else:
        config.html_frame.window.OnLinkClicked(url)
        
    config.html_frame.Show()


def test_or_create_html_frame():
    try:
        # config.html_frame has an Active property
        is_active = config.html_frame.IsActive()
    except wx._core.PyDeadObjectError:
        # HTMLWindow was closed/deleted
        start_html_frame(config.starting_frame)


def action(url):
    # get the address/parameters tuple
    url_data = get_function(url)

    # url decode encoded url slashes
    if len(url_data) >= 5:
        if "_next" in url_data[4]:
            if "%2F" in url_data[4]["_next"]:
                url_data[4]["_next"] = urllib.unquote(url_data[4]["_next"])

    # TODO: unify access_control
    # dictionary examination and RBAC call for any source
    # (RBAC instance method)
    
    # arguments: evt (form submission), controller, function
    
    # access control
    requires_list = set()
    address_item = config.address

    for level in (None, url_data[1], url_data[2]):
        if level is not None:
            address_item = address_item[level]
        if "__rbac" in address_item.keys():
            # look for override top level requirements parameter
            if "override" in address_item["__rbac"].keys():
                if address_item["__rbac"]["override"]:
                    requires_list = set()
            if "requires" in address_item["__rbac"].keys():
                for rb in address_item["__rbac"].get("requires", []):
                    requires_list.add(rb)

    try:
        # Check if access_control is available
        if config.access_control is not None:
            result = config.access_control(requires_list)
            if not result[0]:
                # next line on failed authentication
                # should redirect to an error page or
                # default action
                raise gluon.http.HTTP(403)

        # look for function bound to input address and call it
        # controller functions are called with (evt, args=[], vars={})

        action_data = config.actions["controllers"][url_data[1] \
        ][url_data[2]](None, url_data[3], url_data[4])
        
    except gluon.http.HTTP, e:
        # redirection for auth
        if e.status == 303:
            print "Redirection from", url, "to", e.headers["Location"]
            # incomplete:
            new_url_data = get_function(e.headers["Location"])

            # auth redirection
            if "user" in new_url_data[2]:
                if config._auth_next is None:
                    config._auth_next = url
                    # tmp_url = get_function(new_url_data)
                    new_url_data[4]["_next"] = config._auth_next
                    config._auth_source = create_address(new_url_data)

                return action(config._auth_source)

            else:
                # just redirect the action to the
                # specified url
                return action(e.headers["Location"])

            #     authenticate with wx widget and
            #     redirect to last action (config._auth_next)
            # else
            #    ...

        else:
            if e.status == 403:
                # catch not authorized and other codes
                return action(URL(a=config.APP_NAME, c="default", f="user", args=["not_authorized",]))

        raise


    if type(action_data) == dict:
        if "_redirect" in action_data:
            return action(action_data["_redirect"])

        elif "_no_render" in action_data:
            if action_data["_no_render"] == True:
                return None

        # TODO:
        # Do not acumulate objects trough actions,
        # do something like erease_action_data()

        # this objects are not used yet
        # they intend to replace web2py environment
        # values like response, ...
        config.response._vars = gluon.storage.Storage()
        config.response._vars.update(**action_data)

        action_data["menu"] = config.menu
        action_data["url_data"] = url_data
        action_data.update(**globals())
        action_data["config"] = config
        action_data["T"] = config.env["T"]
        action_data["session"] = config.current["session"]
        action_data["current"] = config.current
        action_data["request"] = config.current["request"]
        action_data["response"] = config.current["response"]

        # config.context.update(**action_data)
        # add environment names to context
        # config.context["T"] = config.env["T"]

    else:
        # no dictionary returned
        # then send void object
        # to the html widget
        return None

    # search for templates for this action
    # if a view file was created, render action data with it

    xml = None

    filename = url_data[2] + ".html"
    path = os.path.join(config.TEMPLATES_FOLDER, url_data[1])

    try:
        if filename in (os.listdir(path)):
            absolute_path = os.path.join(path, filename)
            xml = gluon.template.render(filename=absolute_path, path=config.TEMPLATES_FOLDER, context = action_data)

    except OSError, e:
        print e
        print "Creating folder %s" % path
        os.mkdir(path)

    if xml is None:
        # generic_view = None
        absolute_path = os.path.join(config.TEMPLATES_FOLDER, "generic.html")
        xml = gluon.template.render(filename = absolute_path, path=config.TEMPLATES_FOLDER,  context = config.context)

    return xml


def set_url(url, kind=None):
    # called after link event ends

    # if url position does not exists (-1)
    # and urls list is empty
    #    add url and increment the index value
    if len(config._urls) < 1:
        config._urls.append(url)
        config._this_url = 0

    elif kind=="previous":
        if not (config._this_url <= 0):
            config._this_url -= 1

    elif kind=="next":
        if not(config._this_url >= len(config._urls)):
            config._this_url += 1

    else:
        # new url from the middle of the urls list
        config._urls = config._urls[:(config._this_url+1)]
        config._urls.append(url)
        config._this_url += 1


def get_next_url():
    try:
        url = config._urls[config._this_url +1]
        return url
    except IndexError:
        return None

def get_previous_url():
    try:
        if config._this_url != 0:
            url = config._urls[config._this_url -1]
            return url
        else:
            return None
    except IndexError:
        return None


def load_actions():
    """ Loads controller functions for address/action binding """
    config.actions["controllers"] = dict()
    controllers = __import__('controllers', globals(), locals(),
    ['accounting', 'appadmin', 'crm', 'default', 'fees', 'file',
    'financials', 'migration', 'operations', 'output', 'registration',
    'scm', 'setup'], -1)

    for ct in dir(controllers):
        if not ct.startswith("_"):
            # add to controllers dict
            config.actions["controllers"][ct] = dict()
            tmp_module = getattr(controllers, ct)
            for f in dir(tmp_module):
                if not f.startswith("_"):
                    tmp_object = getattr(tmp_module, f)
                    if callable(tmp_object):
                        if tmp_object.__module__ == "%s.%s" % ("controllers", ct):
                            # add function to the sub-module
                            # dict
                            config.actions["controllers"][ct][f] = getattr(tmp_module, f)


def OnNextClick(evt):
    url = get_next_url()
    if url is not None: return config.html_frame.window.OnLinkClicked(url, kind="next")


def OnPreviousClick(evt):
    url = get_previous_url()
    if url is not None: return config.html_frame.window.OnLinkClicked(url, kind="previous")

def OnHomeClick(evt):
    return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="default", f="index"))


def OnActivatedTool(evt):
    return None

