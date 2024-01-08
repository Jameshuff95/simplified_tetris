from grid import Grid
from blocks import *
# import random is used to return a random block from self.blocks below
import random
# import pygame, used for music
# ogg files are best for music, mp3 files can cause problems

class Game:
    def __init__(self):
        self.grid = Grid()
        # create a list of all the blocks
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        # create an attribute to hold the current block that is visible on the screen
        # to do this select a random block from each available block
        self.current_block = self.get_random_block()
        # create an attribute to hold the next block that will be visible on the screen
        self.next_block = self.get_random_block()
        # create game_over attribute
        self.game_over = False
        self.score = 0
        # self.rotate_sound = pygame.mixer.Sound("Path to sound file")
        # self.clear_sound = pygame.mixer.Sound("Path to sound file")
        # background music
        # pygame.mixer.music.load("Path to music file")
        # ensure the background music play indefinitely, -1 indicates this
        # pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        # reward points determined by how many lines were cleared
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        # add one point for each time the player moves a block down
        self.score += move_down_points

    def get_random_block(self):
        # If no block is present generate a random block
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        # remove the block to ensure each block is displayed at least once
        self.blocks.remove(block)
        return block

    def move_left(self):
        # Move block left
        self.current_block.move(0, -1)
        # Check if the block is inside the game area
        if self.block_inside() == False or self.block_fits() == False:
            # if not, move the block back inside the game area
            self.current_block.move(0, 1)

    def move_right(self):
        # Move block right
        self.current_block.move(0, 1)
        # Check if the block is inside the game area
        if self.block_inside() is False or self.block_fits() == False:
            # if not, move the block back inside the game area
            self.current_block.move(0, -1)

    def move_down(self):
        # Move block down
        self.current_block.move(1, 0)
        # Check if the block is inside the game area
        if self.block_inside() == False or self.block_fits() == False:
            # if not, move the block back inside the game area
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        # update the game grid values to represent the location of each cell of the block
        # and the time it touches the bottom of the grid
        # for each cell store the id of the block in the corresponding cell on the grid
        # get the current positions of all the tiles of the block
        tiles = self.current_block.get_cell_positions()
        # store the id of the block in the corresponding grid cell
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        # spawn a new block on the screen
        self.current_block = self.next_block
        # update next_block attribute to a random new block
        self.next_block = self.get_random_block()
        # call the score method
        rows_cleared = self.grid.clear_full_rows()
        # if rows_cleared > 0:
        # INDENT ME and line below IF UNCOMMENTED self.clear_sound.play()
        self.update_score(rows_cleared, 0)
        # call the clear_rows method
        self.grid.clear_full_rows()
        # check if the new block fits in the grid, if not game over
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    # check every cell oof the block to check if the block is on top of an empty block on the grid or not
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    # Create the rotate method
    def rotate(self):
        self.current_block.rotate()
        # check if block is within the game window, if not undo the rotation
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        # else:
            # self.rotate_sound.play()

    # Check if a block is inside the game window using the is_inside method in grid.py
    def block_inside(self):
        # Get the list of all the tiles
        tiles = self.current_block.get_cell_positions()
        # Check if any tile is outside the grid
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    # Draw the objects on the screen
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)
