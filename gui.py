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

""" IMPORTANT:
replace the normal response, session, ... in web2py views with

config.session, config.response, config.session, ...

"""


# method overriding for handling click on links
class NewHtmlWindow(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        # reload html in html widget (incomplete)
        
        if isinstance(link, basestring):
            print "The link called is " + link
            xml = action(link)
            config.html_frame.window.SetPage(xml)
        else:
            print "The link clicked is " + link.Href
            if not link.Href.startswith("/gestionlibre/"):
                wx.html.HtmlWindow.OnLinkClicked(self, link)
            else:
                xml = action(link.Href)
                config.html_frame.window.SetPage(xml)


def action(url):
    url_data = get_function(url)
    # arguments: evt (form submission), controller, function
    action_data = address[url_data[1]][url_data[2]]["action"](None, url_data[3], url_data[4])
    
    context = None
    
    if "_redirect" in action_data:
        print "redirecting to %s" % action_data["_redirect"]
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
            print "Template file found: " + filename
            absolute_path = os.path.join(path, filename)
            xml = gluon.template.render(filename=absolute_path, path=config.TEMPLATES_FOLDER, context = config.context)
            # print "template HTML"
            # print xml

            # TODO: do the extend / includes parsing

    except OSError, e:
        print e
        print "Creating folder %s" % path
        os.mkdir(path)

    if xml is None:
        # generic_view = None
        absolute_path = os.path.join(config.TEMPLATES_FOLDER, "generic.html")
        xml = gluon.template.render(filename = absolute_path, path=config.TEMPLATES_FOLDER,  context = config.context)


    return xml
