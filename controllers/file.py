# -*- coding: utf-8 -*-

# from gluon import *
import config
T = config.env["T"]

def quit(evt, args=[], vars={}):
    # close all windows
    print T("Session closed by user input")
    config.html_frame.Close()
    # send a _no_render key/value
    # to avoid template render after
    # closing windows
    return dict(_no_render=True)

