import maya.cmds as cmds
import GUI_Button
import Grid
import os

'''
                                THE GUI OF THE PROJECT

This file holds a class that is the main gui window.
The class holds the instance, title, and size of the window. 
Additionally, it holds an instance of the Grid class. And the axis of the grid and 
two stacks of states of the grid. 

The class holds all the manipulations of the GUI window.
'''
class Creation_Window(object):
    def __init__(self):        
        self.window = "Drawing_Window"
        self.title = "Drawing Window"
        self.window_size = [800,640]

        self.Grid = None 
        self.axis = 0
        self.undo_lst = []
        self.redo_lst = []
    
    def define_window(self, *args):
        #delete the window if its already there 
        try:
            cmds.deleteUI(self.window, window=True)
            cmds.windowPref(self.window, remove=True)
        except Exception as e:
            print(f"Opening UI")

        '''
        Upload the images for the GUI
        '''
        script_directory = os.path.dirname(__file__)
        build_path = os.path.join(script_directory, "Build.png")
        circle_path = os.path.join(script_directory, "Circle.png")
        clear_path = os.path.join(script_directory, "Clear.png")
        close_path = os.path.join(script_directory, "Close.png")
        contour_path = os.path.join(script_directory, "Contour.png")
        depth_path = os.path.join(script_directory, "Depth.png")
        erase_path = os.path.join(script_directory, "Eraser.png")
        fill_path = os.path.join(script_directory, "Filler.png")
        line_path = os.path.join(script_directory, "Line.png")
        redo_path = os.path.join(script_directory, "Redo.png")
        reset_path = os.path.join(script_directory, "Reset.png")
        square_path = os.path.join(script_directory, "Square.png")
        triangle_path = os.path.join(script_directory, "Triangle.png")
        undo_path = os.path.join(script_directory, "Undo.png")
        XY_path = os.path.join(script_directory, "XY_plane.png")
        XZ_path = os.path.join(script_directory, "XZ_plane.png")
        YZ_path = os.path.join(script_directory, "YZ_plane.png")
        questions_path = os.path.join(script_directory, "questions.png")
        

        #define blank window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.window_size, sizeable = False)
        tab_form = cmds.formLayout()

        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(tab_form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
            
        main_layout = cmds.columnLayout(adjustableColumn=True, bgc=(0.678 , 0.541 , 0.341), parent=tabs)

        cmds.columnLayout(adjustableColumn=True)

        '''
        Grid layout for the canvas
        '''
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnWidth2=[self.window_size[0]/2, 150], columnAlign2=["left", "right"])

        cmds.columnLayout(adjustableColumn=True)

        grid_lst = []
        grid_size = 20
        cmds.gridLayout(numberOfColumns=grid_size, cellWidthHeight=(self.window_size[0]/(grid_size*2), self.window_size[1]/grid_size - 10))

        self.Grid = Grid.Grid(grid_lst, grid_size)

        for z in range(-grid_size//2, grid_size//2):
            for x in range(-grid_size//2, grid_size//2):
                button = GUI_Button.Grid_button(x,z,self.Grid, self)
                grid_lst.append(button)

        self.Grid.grid = grid_lst
        self.save_state()
        cmds.setParent("..") #close grid layout

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnWidth2=[self.window_size[0]/3, 150], columnAlign2=["left", "right"])
        cmds.iconTextButton(style="iconOnly", label = "Undo", image=undo_path, width=100,height=50, command=lambda *args: self.undo())
        cmds.iconTextButton(style="iconOnly", label = "Redo", image=redo_path, width=100,height=50, command=lambda *args: self.redo())
        cmds.setParent("..") #close rowlayout
        cmds.setParent("..") #close column layout

        '''
        Collapsible Menus next to the grid
        '''
        cmds.columnLayout(adjustableColumn=True)

        '''
        Menu for location
        '''
        cmds.frameLayout("location", label="Location", bgc=(0.35, 0.25, 0.10), width=200, collapsable=True, collapse=True)
        cmds.columnLayout(adjustableColumn=True)

        #position
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 120, 120), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        # Create three float fields
        x_pos = cmds.floatFieldGrp(label="X: ", value1=0.0, columnWidth2=(30, 60))
        y_pos = cmds.floatFieldGrp(label="Y: ", value1=0.0, columnWidth2=(30, 60))
        z_pos = cmds.floatFieldGrp(label="Z: ", value1=0.0, columnWidth2=(30, 60))
        
        cmds.setParent("..")#close rowlayout

        #axis
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(120, 120, 120), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        cmds.iconTextButton(style="iconOnly", label = "XZ", image=XZ_path, width=100,height=50,
                            command=lambda *args: self.change_axis("XZ"))
        cmds.iconTextButton(style="iconOnly", label = "YZ", image=YZ_path, width=100,height=50,
                            command=lambda *args: self.change_axis("YZ"))
        cmds.iconTextButton(style="iconOnly", label = "XY", image=XY_path, width=100,height=50,
                            command=lambda *args: self.change_axis("XY"))

        cmds.setParent("..")#close roylayout
        cmds.setParent("..")#close column
        cmds.setParent("..")#close frame
        '''
        Menu for the Presents
        '''
        cmds.frameLayout("presets", label="Presets", bgc=(0.35, 0.25, 0.10), collapsable=True, collapse=True)

        cmds.columnLayout(adjustableColumn=True)
        
        
        main_form = cmds.formLayout()
        c_button = cmds.iconTextButton(style="iconOnly", label = "Circle", image=circle_path, width=100,height=50,
        command=lambda *args: self.shape(0, input_radius))
        s_button = cmds.iconTextButton(style="iconOnly", label = "Square", image=square_path, width=100,height=50,
        command=lambda *args: self.shape(1, input_radius))
        t_button = cmds.iconTextButton(style="iconOnly", label = "Triangle", image=triangle_path, width=100,height=50,
        command=lambda *args: self.shape(2, input_radius))
        
        cmds.formLayout(main_form, edit=True,
                attachForm=[(c_button, 'left', 10), (c_button, 'top', 10),
                            (t_button, 'right', 10), (t_button, 'top', 10),
                            (s_button, 'top', 10)],
                attachPosition=[(s_button, 'left', 30, 30)])
        cmds.setParent("..") #close rowlayout

        form = cmds.formLayout()
        input_radius = cmds.intSliderGrp(label="radius", min=1, max=8, value=4)
        cmds.formLayout(form, edit=True,
                    attachForm=[(input_radius, 'top', 10)],
                    attachPosition=[(input_radius, 'left', 5, 10)])
        
        cmds.setParent("..")#close formlayout
        
        cmds.setParent("..") #closes column layout inside dropdown menu
        cmds.setParent("..") #closes frame layout

        '''
        Menu for tools 
        '''

        cmds.frameLayout("tools", label="Tools", bgc=(0.35, 0.25, 0.10),collapsable=True, collapse=True)
        cmds.columnLayout(adjustableColumn=True)

        # Buttons inside the collapsible menu

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign2=["left", "right"])
        #Depth
        input_depth = cmds.intSliderGrp(label="depth", min=1, max=10, value=1)
        cmds.iconTextButton(style="iconOnly", label = "Depth", image=depth_path, width=100,height=50,
        command=lambda *args: self.Grid.add_depth(input_depth))
        cmds.setParent("..")

        #Fill 
        cmds.iconTextButton(style="iconOnly", label = "Fill", image=fill_path, width=100,height=50,
        command=lambda *args: self.Grid.fill())
        #Line
        cmds.iconTextButton(style="iconOnly", label = "Line", image=line_path, width=100,height=50,
        command=lambda *args: self.Grid.line())

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign2=["left", "right"])
        #Eraser
        input_erase = cmds.intSliderGrp(label="erase", min=0, max=10, value=2)
        cmds.iconTextButton(style="iconOnly", label = "Erase", image=erase_path, width=100,height=50,
        command=lambda *args: self.Grid.erase(input_erase)
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnAlign2=["left", "right"])
        #contour
        input_contour = cmds.intSliderGrp(label="depth", min=1, max=10, value=2)
        cmds.iconTextButton(style="iconOnly", label = "Contour", image=contour_path, width=100,height=50,
        command=lambda *args: self.Grid.add_contour(input_contour))
        cmds.setParent("..")

        #Build
        cmds.iconTextButton(style="iconOnly", label = "Build", image=build_path, width=100,height=50,
        command=lambda *args: self.build(x_pos, y_pos, z_pos))

        cmds.setParent("..")  # Close column layout inside Tools frameLayout
        cmds.setParent("..")  # Close Tools frameLayout
        cmds.setParent("..")  # Close columnLayout for right side
        cmds.setParent("..")  # Close rowLayout for main alignment
        cmds.setParent("..")


        form = cmds.formLayout()
        #reset
        btn_reset = cmds.iconTextButton(style="iconOnly", label = "Reset Canvas", image=reset_path, width=100,height=50,
        command=lambda *args: self.reset())
        #clear 3D
        btn_clear = cmds.iconTextButton(style="iconOnly", label = "Clear 3D", image=clear_path, width=100,height=50,
        command=lambda *args: self.clear())
        #close window
        btn_close = cmds.iconTextButton(style="iconOnly", label = "Close", image=close_path, width=100,height=50,
        command=lambda *args: self.close_window())
        cmds.formLayout(form, edit=True,
                    attachForm=[(btn_reset, 'top', 10), (btn_close, 'top', 10), (btn_clear, 'top', 10)],
                    attachPosition=[(btn_reset, 'left', 5, 10), (btn_clear, 'left', 5, 40), (btn_close, 'left', 5, 70)])
        
        cmds.setParent("..")

        '''
        Questions
        '''
        # Questions Layout within its own formLayout (initially hidden)
        questions_layout = cmds.columnLayout(adjustableColumn=True, bgc=(0.678 , 0.541 , 0.341), parent=tabs)
        cmds.iconTextStaticLabel(style="iconOnly", image=questions_path, parent=questions_layout)
        cmds.setParent("..")#close column
        cmds.setParent("..")#close frame

        cmds.tabLayout(tabs, edit=True, bgc=(0.35, 0.25, 0.10), tabLabel=((main_layout, 'Drawing'), (questions_layout, 'Questions')) )

        #show the window
        cmds.showWindow(self.window)


    def create_window(self, window_name, title, size):
        '''
        Creates a standard window
        This is to use for functions that have pop up windows 
        '''
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)

        window = cmds.window(window_name, title=title, widthHeight=size, sizeable=True)
        cmds.columnLayout(bgc=(0.35, 0.25, 0.10),adjustableColumn=True)

        return window

    def change_axis(self, axis):
        #changes the axis on the 3D plane
        if axis == "XZ":
            self.axis = 0
        elif axis == "XY":
            self.axis = 1
        elif axis == "YZ":
            self.axis = 2

        
    def build (self,x_input,y_input,z_input):
        '''
        Builds the grid that is being described
        '''

        #get the position
        x_pos = cmds.floatFieldGrp(x_input, query=True, value=True)[0]
        y_pos = cmds.floatFieldGrp(y_input, query=True, value=True)[0]
        z_pos = cmds.floatFieldGrp(z_input, query=True, value=True)[0]

        cubes = []  #List of cubes to combine later
        positions = [(b.x, b.z, b.depth) for b in self.Grid.grid if b.clicked]  # List of clicked button positions with depth

        if positions:  #If there are clicked positions to create cubes
            for x, z, depth in positions:
                #Create one cube per button with a height matching the depth
                cube = cmds.polyCube(w=1, h=depth, d=1)[0]

                #Move cube based on the selected axis, adjusting depth to prevent upside-down effect
                if self.axis == 0:  # XZ plane (y is height)
                    cmds.move(x_pos + x, y_pos + depth / 2, z_pos + z, cube)
                elif self.axis == 1:  # XY plane (z is height)
                    #Move depth in the negative z-direction to prevent upside-down orientation
                    cmds.move(x_pos + x, y_pos - z, z_pos + depth / 2, cube)
                    cmds.rotate(90, 0, 0, cube, relative=True) # Rotate to align height along the z-axis
                elif self.axis == 2:  # YZ plane (x is height)
                    cmds.move(x_pos + depth / 2, y_pos - z, z_pos + x, cube)
                    cmds.rotate(0, 0, 90, cube, relative=True)  # Rotate to align height along the x-axis

                cubes.append(cube)
        if cubes:  # Combine cubes if any were created
            # Combine cubes into a single mesh
            merged_cube = cmds.polyUnite(cubes, ch=False)[0]
            # Clean up history and merge vertices to reduce complexity
            cmds.delete(merged_cube, ch=True)
            cmds.polyMergeVertex(merged_cube, d=0.001)
            cmds.select("polySurface*", deselect=True)
        else:
            #pop up if the menu is empty
            window = self.create_window("menuBuild", "Build", (300, 150))
            cmds.text(label="You need to draw something")
            cmds.button(label="Ok", command=lambda *args: cmds.deleteUI(window, window=True))
            cmds.showWindow(window)
   
    def shape(self, shape, input):
        #Preset shapes 
        #circle, square, and triangle -- functions in the grid
        radius = cmds.intSliderGrp(input, query=True, value=True)
        if shape == 0:
            self.Grid.circle(radius)
        elif shape == 1:
            self.Grid.square(radius)
        elif shape == 2:
            self.Grid.triangle(radius)

    def reset_helper(self, window, close):
        #reset the canvas
        if close: 
            for b in self.Grid.grid:
                b.unclick()
            self.save_state()
        cmds.deleteUI(window, window=True)

    def reset(self, *args):
        #open a pop up window asking the user if they want to close the window or not
        window = self.create_window("menuReset", "Reset", (150, 100))
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Are you sure you want to reset Canvas?")
        cmds.button(label="Yes", command=lambda *args: self.reset_helper(window, close=True))
        cmds.button(label="No", command=lambda *args: self.reset_helper(window, close=False))
        
        cmds.showWindow(window)
    
    def clear_helper(self, clear, window):
        #clears the 3D viewport in maya 
        if clear: 
            polygons = cmds.ls(type='mesh')
        
            polygon_transforms = cmds.listRelatives(polygons, parent=True)
            
            if polygon_transforms:
                print("Screen Cleared")
                cmds.delete(polygon_transforms)

        cmds.deleteUI(window, window=True)

    def clear(self, *args):
        #asks the user if they want to clear the 3D viewport or not 
        window = self.create_window("menuClear", "Clear", (100, 100))
        cmds.text(label="Are you sure you want to clear?")
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 100), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.button(label="Yes", command=lambda *args: self.clear_helper(clear=True, window=window))
        cmds.button(label="No", command=lambda *args: self.clear_helper(clear=False, window=window))
        cmds.showWindow(window)
    
    def close_helper(self, window, close):
        #closes the GUI window
        if close: 
            try: 
                cmds.deleteUI(self.window, window=True)
            except Exception as e:
                print(f"No previous UI to close: {e}")
        cmds.deleteUI(window, window=True)
    
    def close_window(self, *args):
        #prompts the user if they want to close the window or not
        window = self.create_window("menuClose", "Close", (150, 100))
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Are you sure you want to close?")
        cmds.button(label="Yes", command=lambda *args: self.close_helper(window=window, close=True))
        cmds.button(label="No", command=lambda *args: self.close_helper(window=window, close=False))
        
        cmds.showWindow(window)
    
    def save_state(self):
        '''save currect state'''
        #saves a list of tupes with the important information of the state
        #only the clicked and depth be changable
        current_state = [(b.clicked, b.depth) for b in self.Grid.grid]
        self.undo_lst.append(current_state)  #Append state to undo list
        self.redo_lst.clear() 

    def undo(self):
        '''Undo last action'''
        if self.undo_lst:
            # Save the current state to redo list before undoing
            current_state = [(b.clicked, b.depth) for b in self.Grid.grid]
            self.redo_lst.append(current_state)

            # Restore the last state from undo list
            last_state = self.undo_lst.pop()
            self.Grid.update(last_state)
        else:
            print("No more actions to undo.")

    def redo(self):
        '''Redo last action'''
        if self.redo_lst:
            # Save the current state to undo list before redoing
            current_state = [(b.clicked, b.depth) for b in self.Grid.grid]
            self.undo_lst.append(current_state)

            # Restore the next state from redo list
            next_state = self.redo_lst.pop()
            self.Grid.update(next_state)
        else:
            print("No more actions to redo.")
