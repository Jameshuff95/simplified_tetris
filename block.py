from colors import Colors
import pygame
from position import Position


# When creating a block class you need to determine what information is stored in each block
class Block:
    def __init__(self, id):
        # create the id attribute to assign each block a unique id
        self.id = id
        # used to store occupied cells for each rotation state of the block
        self.cells = {}
        # set cell_size
        self.cell_size = 30
        # set initial row offset of the block
        self.row_offset = 0
        # set the initial column offset of the block
        self.column_offset = 0
        # set the initial state of the block
        self.rotation_state = 0
        # Create a colors attribute
        self.colors = Colors.get_cell_colors()

    # This method is used to move the block
    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    # modify the positions of all the cells in the block according to the offset
    # calculates the actual position of itself after the offset is applied
    # it's better to have a separate method for this because the positions will need to be recalculated
    # to check for collisions, also avoids repetitive calculations
    # This method returns the positions of the occupied cells with the offset applied in a list
    def get_cell_positions(self):
        # get the cell positions for the current cell state
        tiles = self.cells[self.rotation_state]
        # create new empty list to hold the moved tiles
        moved_tiles = []
        # loop through all the tiles and add the offset to their positions
        # use in draw method below to draw updated block in new position 'tiles = self.get_cell_positions()'
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            # append position to moved_tiles list
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        self.rotation_state += 1
        # check if rotation state is equal to the number of rotation states the block has
        # if rotation state reaches the maximum number of states for each block
        # need to reset to 0, to do this add a conditional check after incrementing the rotation state
        # this approach applies to all blocks in the game
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == - 1:
            self.rotation_state = len(self.cells) - 1

    # Draws block on screen
    # Pass surface as an argument to draw it
    def draw(self, screen, offset_x, offset_y):
        # this line retrieves the list of positions for the current rotation state of the block
        # as determined by the rotation state attribute in blocks.py
        tiles = self.get_cell_positions()
        # to draw the rectangle use a for loop
        for tile in tiles:
            # Create a rectangle for each cell using the pygame.rect() method
            title_rect = pygame.Rect(offset_x + tile.column * self.cell_size,
                                     offset_y + tile.row * self.cell_size,
                                     self.cell_size - 1, self.cell_size - 1)
            # Draw the Rect
            pygame.draw.rect(screen, self.colors[self.id], title_rect)
