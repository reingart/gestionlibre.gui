#! /usr/bin/python
# -*- coding: utf-8 -*-

HELP_TEXT = """
    GestiónLibre setup command options:

    ./setup.py [option 1 [value 1]] ... [option n]

    * --help : Display this text
    * --?: same as help
    
    * --install : Start server/client configuration. It asks for
    the web2py/gui2py folders, db URI, and wether it must install
    the webapp in the current web2py installation. Writes the
    config.ini file with the installation basic parameters

    * --hmac_key [value] : special key for the web2py auth class (use a local
    key for each GestiónLibre project. Use the same key for client
    installations). If not specified, it is configured during
    installation. (used with --install)

    * --client : Configure as client gui application (used with
    --install)

    * --no_web2py_app : Do not install the web2py application
    (used with --install)
    
    * --no_gui : Skip graphical dialogs on installation. Displays
    the installation options in the terminal (used with --install)
    
    * --web2py_path [value] : Absolute path to the local web2py installation
    (used with --install)
    
    * --gui2py_path [value] : Absolute path to the local gui2py installation
    (used with --install)
"""

import sys, os, random
try:
    import readline
except ImportError:
    print "readline feature not supported for user input"

no_web2py_app = False
path_walk = None
GUI2PY_PATH = None
WEB2PY_PATH = None
GUI_BASED = True
CLIENT = False
LEGACY_DB = False
HMAC_KEY = None
LANGUAGE = ""

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

def create_dirs():
    print "Creating subfolders... "
    for subfolder in ["databases",]:
        path = os.path.join(os.getcwd(), subfolder)
        if not os.path.exists(path):
            os.mkdir(path)
    return None

def create_hmac_key():
    # a naive hmac key creator
    hmk="sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a"
    new_hmac_key = "sha512:"
    for i, c in enumerate(hmk):
        if i > 6:
            if c != "-":
                new_hmac_key += random.choice(tuple("0123456789abcdef"))
            else:
                new_hmac_key += c
    return new_hmac_key


def set_values(web2py_path, gui2py_path, gui_based = GUI_BASED, \
client = CLIENT, legacy_db = LEGACY_DB, hmac_key = HMAC_KEY, \
language = LANGUAGE):
    cwd = os.getcwd()
    try:
        login = os.getlogin()
    except AttributeError:
        login = ""

    WEB2PY_PATH = web2py_path
    GUI2PY_PATH = gui2py_path
    
    # set default paths (templates, example_db, ...)

    ini_values = dict(APP_NAME = APP_NAME,
    SYSTEM_USER_NAME = login,
    GUI2PY_APP_FOLDER = cwd,
    GUI2PY_APP_CLIENT = client,
    WEB2PY_APP_NAME = WEB2PY_APP_NAME,
    WEB2PY_FOLDER = WEB2PY_PATH,
    GUI2PY_FOLDER = GUI2PY_PATH,
    WEB2PY_APP_FOLDER = os.path.join(WEB2PY_PATH, "applications", WEB2PY_APP_NAME),
    DATABASES_FOLDER = os.path.join(cwd, "databases"),
    TEMPLATES_FOLDER = os.path.join(cwd, "views"),
    PDF_TEMPLATES_FOLDER = os.path.join(cwd, "pdf_templates"),
    OUTPUT_FOLDER = os.path.join(cwd, "output"),
    DB_URI = r'sqlite://storage.sqlite',
    DB_TIMEOUT = -1,
    HMAC_KEY = hmac_key,
    LEGACY_DB = legacy_db,
    LANGUAGE = language)

    # confirm db_uri or change it interactively

    # present a modal widget with connection string confirmation
    confirm_text = "Please confirm db connection string\n%s" % ini_values["DB_URI"]
    
    if gui_based:
        retCode = wx.MessageBox(confirm_text, "db URI Srinng", wx.YES_NO | wx.ICON_QUESTION)
        if retCode == wx.YES:
            confirm_uri_string = "y"
        else:
            confirm_uri_string = "n"
    else:
        confirm_uri_string = raw_input(confirm_text + "\n(y/n):")

    if not confirm_uri_string in ("\n", "Y", "y", None, ""):
        # if change uri is requested
        # prompt for uri
        
        prompt_for_db_uri = "Type a valid web2py db connection URI and press Enter"
        
        if GUI_BASED:
            new_uri_string = wx.GetTextFromUser(prompt_for_db_uri, caption="Input text", default_value=ini_values["DB_URI"], parent=None)
        else:
            new_uri_string = raw_input(prompt_for_db_uri + "\n")
            
        ini_values["DB_URI"] = str(new_uri_string)
        if ini_values["DB_URI"] in ("", None):
            print "Installation cancelled. Db conection string was not specified"
            exit(1)

    demo_key = "sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a"
    
    if hmac_key is None:
        confirm_text = "Do you want to keep the demo hmac key?\n%s" % demo_key
        
        if gui_based:
            retCode = wx.MessageBox(confirm_text, "HMAC KEY", wx.YES_NO | wx.ICON_QUESTION)
            if retCode == wx.YES:
                confirm_hmac = "y"
            else:
                confirm_hmac = "n"
        else:
            confirm_hmac = raw_input(confirm_text + "\n(y/n):")

        if not confirm_hmac.strip() in ("\n", "Y", "y", None, ""):
            # if change hmac is requested
            # prompt for hmac

            prompt_for_hmac = "You can use the random key, type a custom key or type \"new\" to retry"

            user_input_loop = True
            while user_input_loop == True:
                new_random_key=create_hmac_key()
                if GUI_BASED:
                    new_hmac = wx.GetTextFromUser(prompt_for_hmac, caption="Input text", default_value=new_random_key, parent=None)
                else:
                    new_hmac = raw_input(prompt_for_hmac + "\n" + new_random_key + " (Enter)\n").strip()
                    
                if new_hmac == "new":
                    # new key requested
                    continue
                elif new_hmac in (None, ""):
                    if not gui_based:
                        # terminal input accepts the random key
                        ini_values["HMAC_KEY"] = new_random_key
                        user_input_loop = False
                    else:
                        print "Installation cancelled. hmac key was not specified"
                        exit(1)
                else:
                    # store wathever was entered
                    ini_values["HMAC_KEY"] = new_hmac
                    user_input_loop = False

        else:
            # demo key
            ini_values["HMAC_KEY"] = demo_key

    # Change db_timeout for postgres connections
    if "postgres" in ini_values["DB_URI"].lower():
        # for remote db connection closed issue
        # ini_values["DB_TIMEOUT"] = 120000
        pass

    # write config values to config.ini
    print "Writing config values to config.ini"

    with open("config.ini", "w") as config:
        for k, v in ini_values.iteritems():
            config.write(k + "=" + str(v) + "\n")

    # write config values to webappconfig.ini
    # for path search purposes mostly
    if not no_web2py_app:
        print "Writing config values to web2py app"
        if ini_values["WEB2PY_APP_FOLDER"] is not None:
            # TODO: and ...FOLDER has a valid path
            with open(os.path.join(ini_values["WEB2PY_APP_FOLDER"], "private", "webappconfig.ini"), "wb") as webappconfig:
                for k, v in ini_values.iteritems():
                    webappconfig.write(k + "=" + str(v) + "\n")

        # configure sys.path extension in local routes.py web app path
        # create a routes.py at web2py_root/applications/appname
        # write sys.path extension command

        """
        # Not used (webapp routes.py file needs extra configuration at
        # the web2py root routes.py file (routes_app)
        
        with open(os.path.join(ini_values["WEB2PY_APP_FOLDER"], "routes.py"), "wb") as routes_file:
            routes_file.write("# -*- coding: utf-8 -*- \n")
            routes_file.write("import os, sys\n")
            routes_file.write("routes_in = tuple()\n")
            routes_file.write("routes_out = tuple()\n")
            routes_file.write("sys.path.append('%s')\n" % os.path.join(ini_values["GUI2PY_APP_FOLDER"], "modules"))
        """

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

    if not no_web2py_app:
        if (WEB2PY_PATH is not None):
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

            starting_frame.gauge.SetValue(40)
            starting_frame.SetStatusText( \
            "web2py app installation complete. Please restart web2py server")

        else:
            print "Installation cancelled. Could not copy web2py app files."
            exit(1)

    create_dirs()
    result = set_values(WEB2PY_PATH, GUI2PY_PATH, gui_based = GUI_BASED, client = CLIENT, legacy_db = LEGACY_DB)

    if result == True:
        starting_frame.gauge.SetValue(50)
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

    print "Searching for %s path. Please wait." % name
    
    while search_loop:
        try:
            path_info = path_walk.next()
            if name in os.path.basename(path_info[0]) and os.path.isdir(path_info[0]):
                path = path_info[0]
                if not path in paths:
                    paths.append(path_info[0])

        except StopIteration:
            # end of walk reached
            search_loop = False
    return None


command_args = [arg.upper().replace("-", "") for arg in sys.argv]

if "HELP" in command_args or "?" in command_args:
    print HELP_TEXT
    exit(0)

elif "INSTALL" in command_args:
    paths = []
    path_walk = None
    WEB2PY_PATH = None
    GUI2PY_PATH = None

    APP_NAME = "gestionlibre"
    WEB2PY_APP_NAME = "gestionlibre"

    arg_counter = 0

    for arg in sys.argv:
        upper_arg = arg.upper()
        arg_name = upper_arg.replace("-", "")

        arg_counter += 1

        if arg_name == "NO_GUI":
            GUI_BASED = False
            print "No gui mode"

        elif arg_name == "NO_WEB2PY_APP":
            no_web2py_app = True
            print "web2py app installation disabled"

        elif arg_name == "WEB2PY_PATH":
            WEB2PY_PATH = sys.argv[arg_counter]

        elif arg_name == "GUI2PY_PATH":
            GUI2PY_PATH = sys.argv[arg_counter]

        elif arg_name == "WEB2PY_APP_NAME":
            WEB2PY_APP_NAME = sys.argv[arg_counter]

        elif arg_name == "LANGUAGE":
            LANGUAGE = sys.argv[arg_counter]

        elif arg_name == "APP_NAME":
            APP_NAME = sys.argv[arg_counter]

        elif arg_name == "CLIENT":
            CLIENT = True

        elif arg_name == "LEGACY_DB":
            LEGACY_DB = True

        elif arg_name == "HMAC_KEY":
            HMAC_KEY = sys.argv[arg_counter]

    if GUI_BASED:

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
            
            feedback = raw_input("Please specify the absolute path to your web2py installation or press Enter for auto search (it might take a while)\n")
            if feedback:
                WEB2PY_PATH = feedback
            else:
                # Loop trough each folder named web2py in system
                # create paths options
                
                search_folder_path("web2py")
                options = []

                if len(paths) > 0:
                    print
                    print "Select a path for your actual web2py installation:"
                    print "###################################################"

                    for i, option in enumerate(paths):
                        options.append(i)
                        print option, " [%s]" % i
                    print

                    try:
                        choice = int(raw_input("Choose a path index:"))
                        WEB2PY_PATH = paths[choice]
                    except (TypeError, IndexError):
                        print "You chosed an invalid path index"
                        exit(1)
                else:
                    print """
                    Could not find the path for web2py.
                    Please install it or set the path manually with
                    > python setup.py install --WEB2PY_PATH [path]
                    """
                    exit(1)

        # If web2py applications folder found, request write confirmation.
        if not no_web2py_app:
            if raw_input(\
            "Please confirm GestionLibreApp installation at %s (y/n):" \
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

            feedback = raw_input("Please specify the absolute path to your gui2py installation or press Enter for auto search (it might take a while)\n")

            if feedback:
                GUI2PY_PATH = feedback
            else:
                options = []
                search_folder_path("gui2py")

                if len(paths) > 0:
                    print
                    print "Select a path for your actual gui2py installation:"
                    print "###################################################"

                    for i, option in enumerate(paths):
                        options.append(i)
                        print option, " [%s]" % i
                    print

                    try:
                        choice = int(raw_input("Choose a path index:"))
                        GUI2PY_PATH = paths[choice]
                    except (TypeError, IndexError):
                        print "You chosed an invalid path index"
                        exit(1)
                else:
                    print """
                    Could not find the path for gui2py.
                    Please install it or set the path manually with
                    > python setup.py install --GUI2PY_PATH [path]
                    """
                    exit(1)
                    
        create_dirs()
        result = set_values(WEB2PY_PATH, GUI2PY_PATH, gui_based = GUI_BASED, client = CLIENT, legacy_db = LEGACY_DB)
        
        if result == True:
            exit(0)
        else:
            exit(1)

else:
    print "Run python setup.py --install for initial setup"
    exit(0)

