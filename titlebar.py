import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTTOM, LEFT, RIGHT, X, Y
from ctypes import windll

tk_title = "Titlebar Demo"

root = tk.Tk()
root.overrideredirect(True)
root.geometry("400x400")
root.geometry('400x400+100+100')
root.title(tk_title)

root.minimized = False # only to know if root is minimized
root.maximized = False # only to know if root is maximized

title_bar = ttk.Frame(root)

# Set the initial theme
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "light")

def change_theme():
    if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
        root.tk.call("set_theme", "light")
    else:
        root.tk.call("set_theme", "dark")

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

close_button = ttk.Button(title_bar, text='  ×  ', command=root.destroy, style="Close.TButton")
expand_button = ttk.Button(title_bar, text=' 🗖 ', command=maximize_window)
minimize_button = ttk.Button(title_bar, text=' 🗕 ',command=minimize_window)
title_bar_title = ttk.Label(title_bar, text=tk_title)

title_bar.pack(fill=X)
close_button.pack(side=RIGHT, padx=5, pady=5)
expand_button.pack(side=RIGHT, padx=0, pady=5)
minimize_button.pack(side=RIGHT, padx=5, pady=5)
title_bar_title.pack(side=LEFT, padx=(10,0))

title_bar.bind('<Button-1>', get_pos)
title_bar_title.bind('<Button-1>', get_pos)

big_frame = ttk.Frame(root)
big_frame.pack(fill="both", expand=True)

root.bind("<FocusIn>",deminimize)
root.after(10, lambda: set_appwindow(root))

resizex_widget = tk.Frame(big_frame,cursor='sb_h_double_arrow')
resizex_widget.pack(side=RIGHT,ipadx=2,fill=Y)
def resizex(event):
    xwin = root.winfo_x()
    difference = (event.x_root - xwin) - root.winfo_width()
    if root.winfo_width() > 150 : # 150 is the minimum width for the window
        try:
            root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
        except:
            pass
    else:
        if difference > 0: # so the window can't be too small (150x150)
            try:
                root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
            except:
                pass
resizex_widget.bind("<B1-Motion>",resizex)

resizey_widget = tk.Frame(big_frame,cursor='sb_v_double_arrow')
resizey_widget.pack(side=BOTTOM,ipadx=2,fill=X)
def resizey(event):
    ywin = root.winfo_y()
    difference = (event.y_root - ywin) - root.winfo_height()
    if root.winfo_height() > 150: # 150 is the minimum height for the window
        try:
            root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
        except:
            pass
    else:
        if difference > 0: # so the window can't be too small (150x150)
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass
resizey_widget.bind("<B1-Motion>",resizey)

# Remember, you have to use ttk widgets
button = ttk.Button(big_frame, text="Change theme!", command=change_theme)
button.pack()

root.mainloop()