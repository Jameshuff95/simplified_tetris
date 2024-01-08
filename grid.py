import pygame
from colors import Colors


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        # Use list comprehension to create a grid full of empty cells, assigned 0 as empty.
        # Each of the 7 colors will be assigned a number in the grid when the piece lands
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    # This code iterates over every grid cell and prints the
    # state of the cell in the console, whether it is empty or not
    # This can be used to see state of each cell in the grid at any time
    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()

    # check if the cells of the grid are occupied
    # if not empty, undo the cells and lock the block on the grid
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    # Write a method to check if a row is full
    def is_row_full(self, row):
        # check if any cell in the row has a value of 0
        for column in range(self.num_cols):
            # check if the value of the cell is o
            if self.grid[row][column] == 0:
                return False
        return True

    # Create a method that will clear the completed row, setting values to 0
    # two arguments, row to move down and how many rows to move down
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    # Create a method to move uncompleted rows down
    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            # change values of destination row to current row
            self.grid[row + num_rows][column] = self.grid[row][column]
            # clear the current row
            self.grid[row][column] = 0

    # Create a method to combine the * methods
    # Scan grid from bottom to top to determine if any row is completed
    def clear_full_rows(self):
        completed = 0
        # iterate through each row in grid bottom to top
        # num_row - 1 means it the grid is scanned in an upward direction
        for row in range(self.num_rows - 1, 0, -1):
            # check if current row is full
            if self.is_row_full(row):
                # call clear_row method to clear all the cells in the row
                self.clear_row(row)
                # implement the completed variable to track number of rows completed
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    # create a reset method for resetting the game
    def reset(self):
        # look through all the cells and set the values to 0
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    # If a given tile position is inside the grid
    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    # Draw each cell in the grid a specific color
    # This code iterates through each cell and assigns it a value of the variable cell_value
    # screen must be added to the method because the Grid class is not in the same file as the main file
    def draw(self, screen):
        # Use a nested for loop to get the value in each cell of the grid
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                # Create rect to contain the cell
                # Rect takes 4 arguments: x-position, y-position, width, height
                # Multiply height and width by cell_size since a grid id being used
                # +1 is added to height and width to create 1px offset in each cell
                # -1 is subtracted to height and width to create 1px border in each cell
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11,
                                        self.cell_size - 1, self.cell_size - 1)
                # The pygame.draw.rect() method requires 3 arguments: rect(surface, color, rect)
                # Uses the cell_value as an index in the colors list
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
