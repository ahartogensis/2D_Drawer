import maya.cmds as cmds

import sys

new_path = '/Users/alexia/Desktop/School/Programming for animators/gui_project/scripts'
if new_path not in sys.path:
    sys.path.append(new_path)

import GUI_Button
import GUI_Window
import Grid

import importlib
importlib.reload(GUI_Button)
importlib.reload(GUI_Window)
importlib.reload(Grid)


import maya.cmds as cmds

Window = GUI_Window.Creation_Window()
Window.define_window()
