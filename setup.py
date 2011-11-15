#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
try:
    import readline
except ImportError:
    print "readline feature not supported for user input"

path_walk = None
GUI2PY_PATH = None
WEB2PY_PATH = None

try:
    import wx

except ImportError:
    print "wxPython not found. Please install wxPython first."
    exit(1)

# wxGlade pre-made setup frame
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.starting_frame_statusbar = \
        self.CreateStatusBar(1, 0)
        self.bitmap_1 = wx.StaticBitmap(self, \
        -1, wx.Bitmap("images/setup_logo.png", wx.BITMAP_TYPE_ANY))
        self.button_start = wx.Button(self, -1, "Install")
        self.panel = wx.Panel(self, -1)
        self.count = 0
        self.gauge = wx.Gauge(self.panel, -1, 50, \
        (0, 0), (480, 25))
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(u"GestiónLibre Setup")
        self.starting_frame_statusbar.SetStatusWidths( \
        [-1])
        # statusbar fields
        starting_frame_statusbar_fields = ["Status bar text"]
        for i in range(len(starting_frame_statusbar_fields)):
            self.starting_frame_statusbar.SetStatusText( \
            starting_frame_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add(self.bitmap_1, 0, 0, 0)
        sizer_1.Add((20, 20))
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_2.Add(self.button_start, 0, 0, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_2.Add(self.panel, 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add((20, 20))

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade


def set_values(web2py_path, gui2py_path):
    cwd = os.getcwd()
    try:
        login = os.getlogin()
    except AttributeError:
        login = None

    # demo key
    HMAC_KEY = "sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a"
    
    WEB2PY_PATH = web2py_path
    GUI2PY_PATH = gui2py_path
    
    # set default paths (templates, example_db, ...)

    ini_values = dict(APP_NAME = APP_NAME,
    SYSTEM_USER_NAME = login,
    WEB2PY_APP_NAME = WEB2PY_APP_NAME,
    WEB2PY_FOLDER = WEB2PY_PATH,
    GUI2PY_FOLDER = GUI2PY_PATH,
    WEB2PY_APP_FOLDER = os.path.join(WEB2PY_PATH, "applications", WEB2PY_APP_NAME),
    SQLITE_DB_FOLDER = os.path.join(WEB2PY_PATH, "applications", WEB2PY_APP_NAME, "databases"),
    TEMPLATES_FOLDER = os.path.join(cwd, "views"),
    PDF_TEMPLATES_FOLDER = os.path.join(cwd, "pdf_templates"),
    OUTPUT_FOLDER = os.path.join(cwd, "output"),
    SQLITE_DB_FILE = r'sqlite://storage.sqlite',
    HMAC_KEY = HMAC_KEY,
    LANGUAGE = "")

    # write config values to config.ini
    print "Writing config values to config.ini"

    with open("config.ini", "w") as config:
        for k, v in ini_values.iteritems():
            config.write(k + "=" + v + "\n")

    # exit with status 0 and message
    print "Installation finished."
    print "You can run GestionLibre from %s with >python main.py" \
    % cwd
    
    return True


def start_install(evt):
    # set status bar text with message "web2py path"
    starting_frame.SetStatusText( \
    "web2py installation path")

    wx.MessageDialog(None, \
    "Please specify your web2py installation folder",
            'web2py folder', wx.OK).ShowModal()

    ddlg_web2py = wx.DirDialog(starting_frame, \
    message="web2py installation path", defaultPath=os.getcwd())

    searching = True
    while searching == True:
        if ddlg_web2py.ShowModal() == wx.ID_OK:
            # assign path to WEB2PY_PATH
            starting_frame.SetStatusText(\
            "web2py path set to " + ddlg_web2py.GetPath())

            WEB2PY_PATH = ddlg_web2py.GetPath()

            starting_frame.gauge.SetValue(10)
            break

        else:
            # action cancelled
            # show modal dialog for exit

            dlg = wx.MessageDialog(None, \
            "Do you want to continue (you must specify web2py path first)?",
            'Re-enter web2py path', wx.YES_NO | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()

            if (retCode == wx.ID_YES):
                dlg.Destroy()
                continue
            else:
                print "Installation cancelled by user input"
                dlg.Destroy()
                searching = False
                starting_frame.Close()
                GestionLibreSetup.Exit()
                exit(1)


    # set status bar text with message "gui2py path"
    starting_frame.SetStatusText("gui2py installation path")

    wx.MessageDialog(None, \
    "Please specify your gui2py installation folder",
            'gui2py path', wx.OK).ShowModal()

    ddlg_gui2py = wx.DirDialog(starting_frame, \
    message="gui2py installation path", defaultPath=os.getcwd())

    searching = True

    global GUI2PY_PATH
    
    
    while searching == True:
        if ddlg_gui2py.ShowModal() == wx.ID_OK:
            # assign path to GUI2PY_PATH
            starting_frame.SetStatusText("gui2py path set to " \
            + ddlg_gui2py.GetPath())
            GUI2PY_PATH = ddlg_gui2py.GetPath()
            starting_frame.gauge.SetValue(20)
            break

        else:
            # action cancelled
            # show modal dialog for exit

            dlg = wx.MessageDialog(None, \
            "Do you want to continue (you must specify gui2py path first)?",
            'Re-enter gui2py path', wx.YES_NO | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()
            if (retCode == wx.ID_YES):
                dlg.Destroy()
                continue
            else:
                print "Installation cancelled by user input"
                dlg.Destroy()
                searching = False
                starting_frame.Close()
                GestionLibreSetup.Exit()
                exit(1)

    if WEB2PY_PATH is not None:
        dlg = wx.MessageDialog(None, \
        "Confirm web2py app installation at %s?" \
        % os.path.join(WEB2PY_PATH, "applications", \
        WEB2PY_APP_NAME),
        'Confirm web2pyapp installation', \
        wx.YES_NO | wx.ICON_QUESTION)
        retCode = dlg.ShowModal()
        if (retCode == wx.ID_YES):
            dlg.Destroy()

        else:
            print "Could not install web2pyapp. Installation cancelled"
            dlg.Destroy()
            searching = False
            starting_frame.Close()
            GestionLibreSetup.Exit()
            exit(1)

        print "Writing web2py app to disk"
        import tarfile

        tf = tarfile.open( \
        "web2py.app.gestionlibre.w2p")
        tf.extractall(path=os.path.join( \
        WEB2PY_PATH, "applications", WEB2PY_APP_NAME))
        tf.close()

        starting_frame.gauge.SetValue(50)
        starting_frame.SetStatusText( \
        "web2py app installation complete. Please restart web2py server")

    else:
        print "Installation cancelled. Could not copy web2py app files."
        exit(1)

    result = set_values(WEB2PY_PATH, GUI2PY_PATH)

    if result == True:
        starting_frame.SetStatusText( \
        "Setup complete")
        starting_frame.button_start.Enable(False)

        wx.MessageDialog(None, \
    u"Setup completed successfully", "Setup complete", wx.OK).ShowModal()


def search_folder_path(name):
    global path_walk
    if path_walk is None:
        path_walk = os.walk("/")

    search_loop = True

    print "Searching for %s path" % name
    
    while search_loop:
        try:
            path_info = path_walk.next()
            if name in path_info[0]:
                path = os.path.join(path_info[0])
                if not path in paths:
                    paths.append( path_info[0] )
                    return path
                    
        except StopIteration:
            # end of walk reached
            search_loop = False
            
    return None


if ("install" in sys.argv) or ("--install" in sys.argv):
    paths = []
    path_walk = None
    WEB2PY_PATH = None
    GUI2PY_PATH = None
    
    APP_NAME = "gestionlibre"
    WEB2PY_APP_NAME = "gestionlibre"

    if not "--no_gui" in sys.argv:
        gui_based = True
    else:
        gui_based = False

    arg_counter = 0
    
    for arg in sys.argv:
        arg_counter += 1

        if arg == "--WEB2PY_PATH":
            WEB2PY_PATH = sys.argv[arg_counter]
            continue

        elif arg == "--GUI2PY_PATH":
            GUI2PY_PATH = sys.argv[arg_counter]
            continue
        
        elif arg == "--web2py_app_name":
            WEB2PY_APP_NAME = sys.argv[arg_counter]
            continue

        elif arg == "--app_name":
            APP_NAME = sys.argv[arg_counter]
            continue


    if gui_based:

        # Install GestionLibre with wxPython interface
        # If WEB2PY_PATH is None
        # ask for web2py path
        # the_evt = fdlg.ShowModal()
        # if fdlg.ShowModal() == wx.ID_OK:
        #    print "Dialog accepted"
        # set web2py_folder
        # Confirm web2py app writing
        # copy GestionLibreApp to web2py applications
        # If GUI2PY_PATH is None
        # ask for gui2py path
        # set gui2py folder

        # start Setup wx window
        GestionLibreSetup = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        starting_frame = MyFrame(None, -1, "")
        starting_frame.SetSize((640, 360))
        GestionLibreSetup.SetTopWindow(starting_frame)
        starting_frame.Bind(wx.EVT_BUTTON, start_install, starting_frame.button_start)
        starting_frame.SetStatusText("GestiónLibre installation utility. Press Install to start")
        starting_frame.Show()
        GestionLibreSetup.MainLoop()


    else:
        # Installation without wxPython Dialogs
        
        if WEB2PY_PATH is None:
            # Search path for web2py installation

            # reset os path walk
            path_walk = None
            the_folder = None
            paths = []
            
            # Loop trough each folder named web2py in system
            while True:
                the_folder = search_folder_path("web2py")
                if the_folder is not None:
                    if raw_input("Is %s your web2py path? (y/n):" \
                    % the_folder) in ["y", "Y"]:
                        WEB2PY_PATH = the_folder
                        break

                else:
                    # end of iteration
                    print """
                    Could not find the path for web2py.
                    Please install it or set the path manually with
                    > python setup.py install --WEB2PY_PATH [path]
                    """
                    exit(1)

        # If web2py applications folder found, request write confirmation.
        if raw_input(\
        "Please confirm GestionLibreApp installation at %s (required for database initialization) (y/n):" \
        % os.path.join(WEB2PY_PATH, "applications", WEB2PY_APP_NAME)) in ["y", "Y"]:
            # If write confirmation,
            # copy web2py.app.gestionlibre.w2p files
            # to web2py applications folder
            print "Writing web2py app to disk"
            import tarfile

            tf = tarfile.open("web2py.app.gestionlibre.w2p")
            tf.extractall(path=os.path.join(WEB2PY_PATH, \
            "applications", WEB2PY_APP_NAME))
            tf.close()
            print "App installation complete. Please restart web2py"
            
        else:
            print "Installation cancelled. Could not copy web2py app files."
            exit(1)

        # Loop trough each folder named gui2py in system
        # If gui2py folder found. request confirmation.
        # If confirmation, set the gui2py folder
        # If no confirmation, continue loop
        # if no gui2py folder found, exit with error 1

        if GUI2PY_PATH is None:
            # Search path for gui2py installation

            # reset os path walk
            path_walk = None
            the_folder = None
            paths = []
            # Loop trough each folder named web2py in system
            while True:
                the_folder = search_folder_path("gui2py")
                if the_folder is not None:
                    if raw_input("Is %s your gui2py path? (y/n):" \
                    % the_folder) in ["y", "Y"]:
                        GUI2PY_PATH = the_folder
                        break

                else:
                    # end of iteration
                    print """
                          Could not find the path for gui2py.
                          Please install it or set the path manually with
                          >python setup.py install --GUI2PY_PATH [path]
                          """

                    exit(1)

        result = set_values(WEB2PY_PATH, GUI2PY_PATH)
        if result == True:
            exit(0)
        else:
            exit(1)

else:
    print "Run python setup.py --install for initial setup"
    exit(0)
