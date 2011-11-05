# -*- coding: utf-8 -*-

import config

# Example event handler ( Set config.MAIN_MENU
# dictionary item with "handler": "handlers.MyHandler")

def MyHandler(evt):
    print "event handler MyHandler called with event", evt.Id
    return None
