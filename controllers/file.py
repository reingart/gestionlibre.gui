# -*- coding: utf-8 -*-

# from gluon import *
import config

def quit(evt, args=[], vars={}):
    # close all windows
    print "Session closed by user input"
    config.html_frame.Close()
    return dict()

