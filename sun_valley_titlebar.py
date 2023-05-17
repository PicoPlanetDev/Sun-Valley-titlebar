import tkinter as tk
from tkinter import ttk
from ctypes import windll
from pathlib import Path

env = Path(__file__).parent
try:
	plugin = windll.LoadLibrary(str(env / "plugin64.dll"))
except OSError:
	plugin = windll.LoadLibrary(str(env / "plugin32.dll"))
except:
	pass

def Titlebar(root, main_frame, icon, title_text, minimize, maximize, close, min_width, min_height):
    #region Docstring
    """Creates a titlebar and basic window functions

    Args:
        root (master): Root window for titlebar
        main_frame (master): Main frame of window
        icon (PhotoImage): Tkinter PhotoImage for icon
        title_text (str): Text to display in titlebar
        minimize (bool): Should a minimize button be created?
        maximize (bool): Should a maximize button be created?
        close (bool): Should a close button be created?
        min_width (int): Minimum width of titlebar
        min_height (int): Minimum height of titlebar
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
        else:
            expand_button.config(text=" 🗖 ")
            root.geometry(root.normal_size)

        root.maximized = not root.maximized

    def set_appwindow(mainWindow):
        global hwnd
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        plugin.setwindow(hwnd)
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())

    def get_pos(event):
        if root.maximized == False:
            def move_window(event): # runs when window is dragged
                root.config(cursor="fleur")
                global x, y, hwnd
                try:
                    plugin.move(hwnd, root.winfo_x(), root.winfo_y(), event.x - x, event.y - y) # Use C for speed
                except:
                    pass

            def release_window(event): # runs when window is released
                root.config(cursor="arrow")
                
            def drag_titlebar(event):
                global x, y
                x = event.x
                y = event.y
                
            title_bar.bind('<B1-Motion>', move_window)
            title_bar.bind('<ButtonRelease-1>', release_window)
            title_bar.bind("<ButtonPress-1>", drag_titlebar)
            title_bar_title.bind('<B1-Motion>', move_window)
            title_bar_title.bind('<ButtonRelease-1>', release_window)
            title_bar_title.bind("<ButtonPress-1>", drag_titlebar)
        else:
            expand_button.config(text=" 🗖 ")
            root.maximized = not root.maximized

    # Pack the title bar window
    title_bar.pack(fill=tk.X)

    # Create the title bar buttons
    if close:
        close_button = ttk.Button(title_bar, text='  ×  ', command=root.destroy, style="Close.Titlebar.TButton")
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)
    if maximize:
        expand_button = ttk.Button(title_bar, text=' 🗖 ', command=maximize_window, style="Titlebar.TButton")
        expand_button.pack(side=tk.RIGHT, padx=0, pady=5)
    if minimize:
        minimize_button = ttk.Button(title_bar, text=' 🗕 ',command=minimize_window, style="Titlebar.TButton")
        minimize_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    if icon != None:
        # Create the title bar icon
        title_bar_icon = ttk.Label(title_bar, image=icon)
        title_bar_icon.pack(side=tk.LEFT, padx=(10,0), fill=tk.Y)

    # Create the title bar title
    title_bar_title = ttk.Label(title_bar, text=title_text)
    title_bar_title.pack(side=tk.LEFT, padx=(10,0))

    # Bind events for moving the title bar
    title_bar.bind('<Button-1>', get_pos)
    title_bar_title.bind('<Button-1>', get_pos)

    # Set up the window for minimizing functionality
    root.bind("<FocusIn>",deminimize)
    root.after(10, lambda: set_appwindow(root))

# Menubar class creates a frame for the menubar which is accessed in the Menu class
class Menubar:
    def __init__(self, root):
        self.root = root
        self.menubar_frame = ttk.Frame(root)
        self.menubar_frame.pack(fill=tk.X, pady=(0,10))

# Adds a menubutton to the menubar frame with the text header
# And allows for the menu to be populated with commands and separators
class Menu:
    def __init__(self, menubar, header):
        self.menu = tk.Menu(menubar.menubar_frame)
        self.menubutton = ttk.Menubutton(menubar.menubar_frame, text=header, menu=self.menu, direction="below")
        self.menubutton.pack(side=tk.LEFT, padx=(10,0))

    def add_command(self, label, command=None):
        if command != None: self.menu.add_command(label=label, command=command)
        else: self.menu.add_command(label=label)

    def add_separator(self):
        self.menu.add_separator()
