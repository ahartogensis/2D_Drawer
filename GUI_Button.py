import maya.cmds as cmds

'''
                                GRID BUTTONs

This file holds the class for the grid buttons. 
It holds instances of the grid and gui it belongs to
There is a set color for unclicked and clicked buttons. 
The values that change is depth, clicked boolean, and color
'''
class Grid_button(object):
    def __init__(self,x,z,grid, gui):
        self.unclicked_c = [1.0, 0.992, 0.816]
        self.clicked_c = [0.85, 0.75, 0.60]
        self.color = self.unclicked_c
        self.depth = 1
        self.grid = grid
        self.gui = gui

        self.button = cmds.button(label="", actOnPress = True, backgroundColor=self.color,
                                  command=lambda *args: self.click(self.grid.depth))

        self.x = x
        self.z = z
        self.clicked = False
    

    def color_change(self):
        #change the color of the button to self.color
        cmds.button(self.button, edit=True, backgroundColor=self.color)
        
    def click(self, d=1, updating=False):
        self.depth = d #adds depth
        self.color = [self.clicked_c[0] - (self.depth - 1) * .08, self.clicked_c[1] - (self.depth - 1) * .08, self.clicked_c[2] - (self.depth - 1) * .08]
        self.clicked = True #set to click
        self.color_change()
        self.grid.set_last_button(self) #sets the last clicked button
        if updating==False: #if it is updating then the state is saved 
            self.gui.save_state()
   
    def unclick(self):
        #unclicks the button
        self.clicked = False
        self.color = self.unclicked_c
        self.color_change()
