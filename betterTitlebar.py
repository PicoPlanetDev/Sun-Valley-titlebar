import tkinter as tk
from tkinter import ttk
from ctypes import windll

def Titlebar(root, mainFrame, theme, titleText, minimize, maximize, close, minWidth, minHeight):
    #region Docstring
    """Creates a titlebar and basic window functions

    Args:
        root (master): Root window for titlebar
        mainFrame (master): Main frame of window
        theme (str): Theme for titlebar, can be 'light' or 'dark'
        titleText (str): Text to display in titlebar
        minimize (bool): Should a minimize button be created?
        maximize (bool): Should a maximize button be created?
        close (bool): Should a close button be created?
        minWidth (int): Minimum width of titlebar
        minHeight (int): Minimum height of titlebar
    """
    #endregion
    
    root.minimized = False # only to know if root is minimized
    root.maximized = False # only to know if root is maximized

    # Create a frame for the titlebar
    title_bar = ttk.Frame(root)

    # Window manager functions
    def minimize_window():
        root.attributes("-alpha",0)
        root.minimized = True       

    def deminimize(event):
        root.focus() 
        root.attributes("-alpha",1)
        if root.minimized == True:
            root.minimized = False                              

    def maximize_window():
        if root.maximized == False:
            root.normal_size = root.geometry()
            expand_button.config(text=" 🗗 ")
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
            root.maximized = not root.maximized         
        else:
            expand_button.config(text=" 🗖 ")
            root.geometry(root.normal_size)
            root.maximized = not root.maximized

    def set_appwindow(mainWindow):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())

    def get_pos(event):
        if root.maximized == False:
            
            xwin = root.winfo_x()
            ywin = root.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event): # runs when window is dragged
                root.config(cursor="fleur")
                root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


            def release_window(event): # runs when window is released
                root.config(cursor="arrow")
                
            title_bar.bind('<B1-Motion>', move_window)
            title_bar.bind('<ButtonRelease-1>', release_window)
            title_bar_title.bind('<B1-Motion>', move_window)
            title_bar_title.bind('<ButtonRelease-1>', release_window)
        else:
            expand_button.config(text=" 🗖 ")
            root.maximized = not root.maximized

    # Pack the title bar window
    title_bar.pack(fill=tk.X)

    # Create the title bar buttons
    if close:
        close_button = ttk.Button(title_bar, text='  ×  ', command=root.destroy, style="Close.TButton")
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)
    if maximize:
        expand_button = ttk.Button(title_bar, text=' 🗖 ', command=maximize_window)
        expand_button.pack(side=tk.RIGHT, padx=0, pady=5)
    if minimize:
        minimize_button = ttk.Button(title_bar, text=' 🗕 ',command=minimize_window)
        minimize_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Create the title bar title
    title_bar_title = ttk.Label(title_bar, text=titleText)
    title_bar_title.pack(side=tk.LEFT, padx=(10,0))

    # Bind events for moving the title bar
    title_bar.bind('<Button-1>', get_pos)
    title_bar_title.bind('<Button-1>', get_pos)

    # Set up the window for minimizing functionality
    root.bind("<FocusIn>",deminimize)
    root.after(10, lambda: set_appwindow(root))

    #region Set up resizing functionality
    resizex_widget = tk.Frame(mainFrame,cursor='sb_h_double_arrow')
    resizex_widget.pack(side=tk.RIGHT,ipadx=2,fill=tk.Y)
    def resizex(event):
        xwin = root.winfo_x()
        difference = (event.x_root - xwin) - root.winfo_width()
        if root.winfo_width() > minWidth:
            try:
                root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
            except:
                pass
        else:
            if difference > 0:
                try:
                    root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
                except:
                    pass
    resizex_widget.bind("<B1-Motion>",resizex)

    resizey_widget = tk.Frame(mainFrame,cursor='sb_v_double_arrow')
    resizey_widget.pack(side=tk.BOTTOM,ipadx=2,fill=tk.X)
    def resizey(event):
        ywin = root.winfo_y()
        difference = (event.y_root - ywin) - root.winfo_height()
        if root.winfo_height() > minHeight:
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass
        else:
            if difference > 0:
                try:
                    root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
                except:
                    pass
    resizey_widget.bind("<B1-Motion>",resizey)
    #endregion