# Sun Valley Titlebar

## Appearance
![TitlebarDemo](https://user-images.githubusercontent.com/50522829/132222258-7a312ef9-d72c-42a7-81dc-69dc9ba592a0.gif)

## Description

This repository provides an easy way to create a custom titlebar that matches rdbende's Sun Valley ttk theme. 
Windows only for right now, it relies on windll to interact with the window manager.

## Usage

**See example.py for a demo**

1. Download the code and place it in your project. You must use the version of the Sun Valley theme provided here or at my fork of the Sun Valley repository (https://github.com/PicoPlanetDev/Sun-Valley-ttk-theme) or in this pull request (https://github.com/rdbende/Sun-Valley-ttk-theme/pull/5) until the pull request is approved.
2. Import tkinter and ttk
3. Import sun_valley_titlebar
4. Create your tkinter window, making sure a minsize is set and overrideredirect is True
5. Set your theme
6. If you want an icon, define a tkinter PhotoImage to hold the icon
7. Create a content frame, but don't pack it yet
8. Create a titlebar (see syntax below)
9. (Optional) Create a menubar and add menus, commands, and separators (see syntax below)
10. Pack the content frame with fill="Both" and expand="True"
11. Add any content you want in the window to the content frame
12. Run the mainloop

## Syntax

### Titlebar
```python
titlebar = sun_valley_titlebar.Titlebar(
    <ROOT FRAME>, <CONTENT FRAME>, <ICON>, <TITLEBAR TEXT>, <MINIMIZE BUTTON?>, <MAXIMIZE BUTTON?>, <CLOSE BUTTON>, <MINSIZE X>, <MINSIZE Y>
)
```
### Menubar

To create the Menubar frame:
```python
menubar = sun_valley_titlebar.Menubar(<ROOT FRAME>)
```
To add menus:
```python
menu = sun_valley_titlebar.Menu(<MENUBAR OBJECT FROM ABOVE>, <STR MENU HEADER>)
```
To add commands and separators to a menu:
```python
menu.add_command("Exit", root.destroy) # Add a command to exit the program
menu.add_separator() # Add a menu separator
```

## TODO
- Add rounded corner background (files with correct colors and 8px corner radius are already included)
- Allow resizing from both sides
- Fix a bug where *sometimes* (ugh) the window won't re-appear after being minimized

If you complete any of these items, add a pull request and I'll happily include it!

## Credits

Based on code from the following repositories:

https://github.com/rdbende/Sun-Valley-ttk-theme

https://github.com/Terranova-Python/Tkinter-Menu-Bar

Feather icon from Icons8: https://icons8.com/icon/FqJJi4fvAZtu/lightweight"
