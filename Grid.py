import math 
import maya.cmds as cmds

'''
                                GRID

This file holds the class for the grid
It holds a list that is the grid of button objects. And it holds the size. As well as
the current depth used 
And it holds a pointer to the pressed and last pressed buttons. 

All functions that change the grid are in here. 
'''

class Grid:
    def __init__(self, grid, size):
        self.grid = grid
        self.grid_size = size
        self.depth = 1

        self.pressed = None 
        self.last_pressed = None
    
    def update(self, state):
        #update the grid
        for button, state in zip(self.grid, state):
            clicked, depth = state
            #retrieve from the state the click boolean and depth
            #change each button in the current grid
            if clicked == True:
                button.click(depth,True)
            else:
                button.unclick()
            
    
    def add_depth(self, input_depth):
        #add depth to the next set of buttons
        self.depth = cmds.intSliderGrp(input_depth, query=True, value=True)
    
    def set_last_button(self, button):
        #change the pressed button to last pressed
        #and the pressed button to the current one
        self.last_pressed = self.pressed
        self.pressed = button
    
    def get_button(self, x, z):
        #find the closest button to the coordinates 
        closest_button = None
        min_distance = float('inf')

        for button in self.grid:
            distance = math.sqrt((button.x - x)**2 + (button.z - z)**2)
            if distance < min_distance:
                min_distance = distance
                closest_button = button

        return closest_button
    
    def get_neighbors(self, start_button):
        #returns the neighboring buttons from the start button
        #Buttons that are left, right, up, and down  
        neighbors = [
                self.get_button(start_button.x + 1, start_button.z),
                self.get_button(start_button.x - 1, start_button.z),
                self.get_button(start_button.x, start_button.z + 1),
                self.get_button(start_button.x, start_button.z - 1)
            ]
        return neighbors 
    
    def calculate_center(self, clicked_buttons):
        #finds the center of buttons clicked 
        x_total = sum(b.x for b in clicked_buttons)
        z_total = sum(b.z for b in clicked_buttons)
        center_x = x_total / len(clicked_buttons)
        center_z = z_total / len(clicked_buttons)
        return center_x, center_z 
    
    def erase(self, input):
        r = cmds.intSliderGrp(input, query=True, value=True)
        #erase tool 
        #erases in a circle of the recently pressed
        if self.pressed: 
            for b in self.grid:
                distance = math.sqrt((self.pressed.x - b.x) ** 2 + (self.pressed.z - b.z) ** 2)
                if abs(distance <= r):
                    b.unclick()
        else:
            print("need to click where to erase")

    def fill(self):
        ''' 
        
        implementation of a flood fill algorithm
        the function traverses through connecting buttons until it reaches a clicked one
        uses a stack to prevent recursion overflow 

        starts with the button that is pressed 
        '''
        self.pressed.unclick()
        stack = [self.pressed]
        while len(stack) > 0:
            button = stack.pop()
            
            #skip clicked button 
            if button.clicked:
                continue

            button.click(self.depth)
            
            neighbors = self.get_neighbors(button)

            #adds the non clicked neighbors
            for neighbor in neighbors:
                if neighbor and not neighbor.clicked:
                        stack.append(neighbor)
    
    def circle(self, radius):
        #creates a circle with radius
        for button in self.grid:
            distance = math.sqrt((button.x) ** 2 + (button.z) ** 2)
            if abs(distance - radius) <= 0.5:
                button.click(self.depth)

    def square(self, length):
        #creates a square with side of 2*length 
        #length is half of the side of the square 
        for i in range(-length,length + 1):
            if -length < i and i < length:
                self.get_button(i, length).click(self.depth)
                self.get_button(i, -length).click(self.depth)
            
            self.get_button(-length, i).click(self.depth)
            self.get_button(length, i).click(self.depth)

    def triangle(self, length):
        #creates a triangle with 2 * length
        height = length * 2 
        for y in range(height):  #Loop through each row from the top to the bottom of the triangle
            #Left and right edges of the triangle
            self.get_button(-y, y - length).click(self.depth)  #Left edge
            self.get_button(y, y - length).click(self.depth)    #Right edge

            # Bottom edge of the triangle (activate all buttons along the base on the last row)
            if y == height-1:
                for x in range(-y, y + 1):
                    self.get_button(x, y - length).click(self.depth)

    def calculate_straight_curve(self, x1,z1,x2,z2, steps):
        #Determine the step size (either 1 or -1 for both x and z to move in the grid)
        x_diff = x2 - x1
        z_diff = z2 - z1
        x_step = 1 if x_diff > 0 else -1 if x_diff < 0 else 0
        z_step = 1 if z_diff > 0 else -1 if z_diff < 0 else 0

        for step in range(1, steps):
            x = x1 + step * x_step
            z = z1 + step * z_step

            #Find the button at (x, z) and simulate its click
            for button in self.grid:
                if button.x == x and button.z == z:
                    button.click(self.depth)

    def calculate_bezier_curve(self, x1, z1, cx, cz, x2, z2, num_points):
        #calculate if the curve is not straight
        #find the bezier path
        points = []
        points.append((x1,z1))
        for t in range(num_points + 1):
            t = t / num_points
            # Quadratic Bézier curve formula
            x = (1 - t)**2 * x1 + 2 * (1 - t) * t * cx + t**2 * x2
            z = (1 - t)**2 * z1 + 2 * (1 - t) * t * cz + t**2 * z2
            points.append((x, z))
        points.append((x2,z2))

        for (x, z) in points:
            closest_button = self.get_button(x, z)
            if closest_button:
                closest_button.click(self.depth)
    
    def line(self):
        '''
        Creates a line between two buttons pressed
        '''
        if self.pressed and self.last_pressed:
            x1,z1 = self.pressed.x,self.pressed.z
            x2,z2 = self.last_pressed.x,self.last_pressed.z
            
            x_diff = x2 - x1
            z_diff = z2 - z1

            #Get the number of steps between the two points
            steps = max(abs(x_diff), abs(z_diff))
            
            #figures out what type of line you are creating 
            if (x1 == x2 or z1 == z2 or abs(x2 - x1) == abs(z2 - z1)):
                #if it is a straight line, it will create a straight curve
                self.calculate_straight_curve(x1,z1,x2,z2,steps)
            else:
                #if it is a curved line, it will create a curved line 
                # Define a control point P1 to create a curved path
                control_x, control_z = (x1 + x2) / 2, (z1 + z2) / 2 + 2  # Offset for curvature

                # Generate points along the curve
                self.calculate_bezier_curve(x1, z1, control_x, control_z, x2, z2, steps)
        else:
            print("Need to click two points")

    def find_outline(self, clicked_buttons, center_x, center_z):
        outline_buttons = []
        
        for button in clicked_buttons:
            neighbors = self.get_neighbors(button)
            if any(neighbor and not neighbor.clicked for neighbor in neighbors):
                outline_buttons.append(button)
        
        #Find the outline button closest to the center
        closest_button = min(outline_buttons, key=lambda b: math.sqrt((b.x - center_x) ** 2 + (b.z - center_z) ** 2))
        return closest_button

    def add_contour(self, input):
        #add an inner layer of buttons with a set contour
        depth = cmds.intSliderGrp(input, query=True, value=True)
        clicked_buttons = [b for b in self.grid if b.clicked]
        if not clicked_buttons:
            print("No clicked buttons found.")
            return

        center_x, center_z = self.calculate_center(clicked_buttons)
        start_button = self.find_outline(clicked_buttons, center_x, center_z)

        inner_border = []
        stack = [start_button]
        visited = []

        while len(stack) > 0:
            #use a similar flood algorithm as fill
            #but only click on the buttons that have
            #at least one clicked neighbor 
            button = stack.pop()

            visited.append(button)
            is_border = False

            neighbors = self.get_neighbors(button)

            closest_outline = None
            for neighbor in neighbors:
                if neighbor:
                    if neighbor.clicked:
                        closest_outline = neighbor
                        is_border = True
                    elif neighbor not in visited:
                        stack.append(neighbor)

            if is_border and button != start_button:
                if math.sqrt((button.x - center_x) ** 2 + (button.z - center_z) ** 2) <= math.sqrt((closest_outline.x - center_x) ** 2 + (closest_outline.z - center_z) ** 2): 
                    inner_border.append(button)

        for b in inner_border:
            b.click(depth)
       
