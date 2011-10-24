# -*- coding: utf-8 -*-
import wx
import wx.html

from gluon import *
import gluon
import config

from url import get_function

address = config.address

# method overriding for handling click on links
class NewHtmlWindow(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        # reload html in html widget (incomplete)        
        print "The link clicked is " + link.Href

        if not link.Href.startswith("/gestionlibre/"):
            wx.html.HtmlWindow.OnLinkClicked(self, link)
        else:
            xml = action(link.Href)
            config.html_frame.window.SetPage(xml)



def action(url): # , parent, style = WX_HTML_STYLE
    url_data = get_function(url)
    """
    # check if html window obj is not available
    if address[url_data[1]][url_data[2]]["window"] is None:
        # if there is no html window, create it
        # create the HTML "browser" window:
        address[url_data[1]][url_data[2]]["window"] = NewHtmlWindow( \
        parent, style = style)

    else:
        # show actual window
        print "doing nothing (incomplete)"
    """
    # window = address[url_data[1]][url_data[2]]["window"]

    # populate the view with the action dict
    # passing the wx obj for binding, args and vars

    """
    action_data = address[url_data[1]][url_data[2]]["action"]( \
    window, url_data[3], url_data[4])
    """
   
    action_data = address[url_data[1]][url_data[2]]["action"](url_data[3], url_data[4])

    if "_redirect" in action_data:
        print "redirecting to %s" % action_data["_redirect"]
        return action(action_data["_redirect"])

    body = [config.menu,]
    body += [DIV(H3(k), DIV(action_data[k])) for k in action_data]
    
    xml = DIV(body).xml()

    # show generic view (just the list of objects with h3 titles
    # refresh window

    # address[url_data[1]][url_data[2]]["window"].SetPage(divs.xml())
    
    return xml
