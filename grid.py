import pygame
import numpy as np
import random

class Grid:
    #Initialize the grid using a constructor
    def __init__(self, width, height, scale, offset):
        self.scale = scale

        #The number of columns and rows are relative to the scale given
        #Width and Height stay the same (I set them to match the screen), so the scale decide how many rectangles we have
        self.columns = int(height/scale)
        self.rows = int(width/scale)

        self.size = (self.rows, self.columns)
        #I am using the numpy library to create a 2d array
        #Changing the size of an ndarray will create a new array and delete the original, which is convenient for this project
        self.grid_array = np.ndarray(shape=(self.size))
        #Offset is for determining the space between each rectangle
        self.offset = offset
    #Generating a random 2d array with 0 and 1
    def random2d_array(self):
        for x in range(self.rows):
            for y in range(self.columns):
                self.grid_array[x][y] = random.randint(0,1)


    def Conway(self, off_color, on_color, surface):
        for x in range(self.rows):
            for y in range(self.columns):
                #Find the position of x and y on the screen
                y_pos = y * self.scale
                x_pos = x * self.scale
                #Determine the rectangle colors and drawing them using pygame
                if self.grid_array[x][y] == 1:
                    pygame.draw.rect(surface, on_color, [x_pos, y_pos, self.scale-self.offset, self.scale-self.offset])
                else:
                    pygame.draw.rect(surface, off_color, [x_pos, y_pos, self.scale-self.offset, self.scale-self.offset])

        #Draw the array again
        next = np.ndarray(shape=(self.size))
        
        for x in range(self.rows):
            for y in range(self.columns):
                #Determine the current state of each cell one by one
                state = self.grid_array[x][y]
                #Find the neighbours said cell
                neighbours = self.get_neighbours( x, y)
                #If a cell is dead (0) and three of her neighbours are alive, the cell becomes alive (1) in the next grid (or gen)
                if state == 0 and neighbours == 3:
                    next[x][y] = 1
                #If a cell is alive (1) and has less than 2 or more than 3 neighbours alive, it dies (0)
                elif state == 1 and (neighbours < 2 or neighbours > 3):
                    next[x][y] = 0
                #Anything else, the cell stays the same and doesn't change states
                else:
                    next[x][y] = state
        #Pass onto the next generation/grid
        self.grid_array = next

    #Function for adding the numbers of the cells surrounding each cell
    def get_neighbours(self, x, y):
        total = 0
        for n in range(-1, 2):
            for m in range(-1, 2):
                x_edge = (x+n+self.rows) % self.rows
                y_edge = (y+m+self.columns) % self.columns
                total += self.grid_array[x_edge][y_edge]

        total -= self.grid_array[x][y]
        return total