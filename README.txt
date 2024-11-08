-----------------------------------------------------------------------------
                                Alexia Hartogensis
                                    GUI PROJECT
-----------------------------------------------------------------------------

Project made with Maya cmds folder to create a pixel art canvas in Maya that 
translates to the 3D viewport. 

Inside this project, there are four script files: main.py, GUI_Window.py,
Grid.py, and GUI_Button.py. Additionally, the file has images I created in Canva
that get loaded in as textures. 
- main.py 
    The file that loads the other scripts and run them 
- GUI_Window.oy 
    The GUI class, it holds the design and structure of the GUI.
- Grid.py 
    The Grid class, a grid object that is respresented by a list of buttons. 
- GUI_Button.py 
    The Button class, an object for the buttons on the grid. It holds meta data 
    on the button and it's cube form. 

I made a drawing feature where the user can draw anything they 
want on a canvas of buttons and then build the 3D version in the Maya viewport. 
On the side of the canvas, there are multiple tools to help the user draw. 
The main GUI has two tabs, the drawer and questions. In the questions tab, there is
detailed information on how to use the multiple tools. And the tools are labeled with
what they can do. 

Location menu: 
Choose the position (x,y,z) of your mesh
Choose the axis of your mesh

Prest menu: 
preset shapes that you can make on the canvas

Tool menu: 
- The depth slider decides the depth of a button and then the depth button sets it. 
- The fill tool fills the area that you last clicked. 
- The line tool draws a line between the last two points drawn. 
    works for straight lines and curved lines 
- The erase slider choose a radius of the area you want to erase and then the erase
    button erases the last picked area. 
- The contour slider decides the depth of the inner border of any shape. Clicking 
    the contour button will create the border. 
- The build tool will generate the 3D mesh in the Maya viewport 

Additional Controls at the bottom: 
- Undo and Redo 
- Reset Canvas 
- Clear the 3D mesh 
- Close Window 

Bugs: 
There is a bug when filling in a triangle. Instead of completely filling the triangle, 
it will forget the corners and draw a bit on the outside. 
Also there is a bug in the line tool. It can perfectly draw straight and diagonal lines, 
but has difficulty with bezier curves. Sometimes the line won't fully connect. 
