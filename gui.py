# -*- coding: utf-8 -*-
import wx
import wx.html

from gluon import *
import gluon
import config

import os

db = config.db
session = config.session
response = config.response
from url import get_function
address = config.address
import gluon.template

from gestion_libre_wx import MyHTMLFrame, MyDialog, MyFrame

""" IMPORTANT:
replace the normal response, session, ... in web2py views with

config.session, config.response, config.session, ...
"""

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
        
        if isinstance(link, basestring):
            if (link.startswith("/%s" % config.APP_NAME) or \
            link.startswith(config.APP_NAME)):
                xml = action(link)
                config.html_frame.window.SetPage(xml)
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
                config.html_frame.window.SetPage(xml)

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
    url_data = get_function(url)
    # arguments: evt (form submission), controller, function
    try:
        action_data = config.address[url_data[1]][url_data[2]]["action"](None, url_data[3], url_data[4])
    except gluon.http.HTTP, e:
        # redirection for auth
        if e.status == 303:
            print "Redirection from", url, "to", e.headers["Location"]
            # incomplete:
            new_url_data = get_function(e.headers["Location"])
            
            if "user" in new_url_data[2]:
                if config._auth_next is None:
                    config._auth_next = url
                    config._auth_source = "/".join((new_url_data[0], new_url_data[1], new_url_data[2], new_url_data[3][0]))

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
            # TODO: if e.status ...
            # catch not authorized and other codes
            pass
            
        raise

    if "_redirect" in action_data:
        return action(action_data["_redirect"])

    else:
        if type(action_data) == dict:
            config.response._vars.update(**action_data)
            action_data["menu"] = config.menu
            action_data["url_data"] = url_data
            action_data.update(**globals())
            config.context.update(**action_data)

    # search for templates for this action
    # if a view file was created, render action data with it

    xml = None

    filename = url_data[2] + ".html"
    path = os.path.join(config.TEMPLATES_FOLDER, url_data[1])

    try:
        if filename in (os.listdir(path)):
            absolute_path = os.path.join(path, filename)
            xml = gluon.template.render(filename=absolute_path, path=config.TEMPLATES_FOLDER, context = config.context)

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


def OnNextClick(evt):
    url = get_next_url()
    if url is not None: return config.html_frame.window.OnLinkClicked(url, kind="next")


def OnPreviousClick(evt):
    url = get_previous_url()
    if url is not None: return config.html_frame.window.OnLinkClicked(url, kind="previous")

def OnHomeClick(evt):
    return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="default", f="index"))

