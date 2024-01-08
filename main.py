import pygame
import sys
from game import Game
from colors import Colors

# Definitions

# Initialize pygame
pygame.init()

# create a font for the score text
# #None is used to use the default pygame font followed by font size
title_font = pygame.font.Font(None, 40)
# create a surface for the title to be written on
# render("string to display", block_alias, font_color)
score_surface = title_font.render("Score", True, Colors.white)
# render the surface that displays the next block
next_surface = title_font.render("Next", True, Colors.white)
# render the surface that displays the next block
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

# create a rect for which the score to be displayed
score_rect = pygame.Rect(320, 55, 170, 60)
# create a rect for which the next block to be displayed
next_rect = pygame.Rect(320, 215, 170, 180)

# Creates a display surface object, which is a blank canvas on which to draw objects
# The set_mode method takes a tuple as an argument which contains width and height in this case
screen = pygame.display.set_mode((500, 620))

# Use set_caption to give the screen a title
pygame.display.set_caption("Python Tetris")

# Create a clock object to control the frame rate of the game
clock = pygame.time.Clock()

# Create the game object
game = Game()

# Create a timer event using a pygame library
# Create a custom event for the game using the pygame.USEREVENT library
GAME_UPDATE = pygame.USEREVENT
# Use the set_timer event from the pygame.time() module to run GAME_UPDATE every 200ms
pygame.time.set_timer(GAME_UPDATE, 200)


# Game Loop

while True:
    # gets all events and puts them in a list
    for event in pygame.event.get():
        # set up a way to exit the game and break the while loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # add keydown event to be able to move the blocks
        if event.type == pygame.KEYDOWN:
            # use event.key attribute to return a const tht represents a key that is pressed
            if game.game_over == True:
                game.game_over = False
                # to reset the game call the reset method in the game class
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()

        # add a check for the custom event
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()

    # since the score is dynamic, it needs to be updated within the game loop
    # convert to score to a string from an integer so it is displayed on the surface
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    # paint the game screen with the fill() method
    screen.fill(Colors.dark_blue)

    # use the blit method to display the surface for the score
    screen.blit(score_surface, (365, 20, 50, 50))

    screen.blit(next_surface, (375, 180, 50, 50))

    if game.game_over == True:
        screen.blit(game_over_surface, (320, 450, 50, 50))

    # draw the score_rect
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)

    # display the score_value_surface on top of the score_surface
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                  centery=score_rect.centery))

    # draw the next_rect
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)

    # Draw the Game
    game.draw(screen)

    # This line of code takes all changes made in game objects and draws them
    pygame.display.update()

    # tick() takes an integer as an argument that represents the fps
    # Setting the fps isn't necessary, but it ensures consistency in performance
    clock.tick(60)
