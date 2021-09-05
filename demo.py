import tkinter as tk
from tkinter import ttk
from betterTitlebar import Titlebar

tk_title = "Titlebar Demo"

root = tk.Tk()
root.overrideredirect(True)
root.minsize(400, 400)
root.geometry('400x400+100+100')
root.title(tk_title)
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "light")

def change_theme():
    if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
        root.tk.call("set_theme", "light")
    else:
        root.tk.call("set_theme", "dark")

big_frame = ttk.Frame(root)

titlebar = Titlebar(root, big_frame, 'light', tk_title, True, True, True, 400, 400)

big_frame.pack(fill="both", expand=True)

# Remember, you have to use ttk widgets
button = ttk.Button(big_frame, text="Change theme!", command=change_theme)
button.pack()

root.mainloop()