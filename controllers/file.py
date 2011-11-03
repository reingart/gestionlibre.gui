# -*- coding: utf-8 -*-

# from gluon import *
import config

def quit(evt, args=[], vars={}):
    # close all windows
    print "Session closed by user imput"
    config.starting_frame.Close()
    return dict()

