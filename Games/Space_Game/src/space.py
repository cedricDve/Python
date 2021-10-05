import pygame
from pygame.locals import *

# Define fps to set a max. fps: using clock -> pygame.time.Clock()
fps = 60
clock = pygame.time.Clock()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Create a (untitled)game-window:
    # display.set_mode() -> two parameters: width and height 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# --  Add game title: display.set_caption
pygame.display.set_caption("Space Invaders")

# Load images: using -> pygame.image.load
bg_img = pygame.image.load("./images/bg.png")

# Display background image
# Using -> screen.blit() ->> two parameters: image and coordoniates(tuppel: x and y coord.)
def display_bg():    
    # Background image position -> take entire screen => (0,0)
    screen.blit(bg_img,(0,0))
    # Background image will be displayed as first => need to be set as a background, all other images will be displayed above!


# Game loop: game will run until 'run != true'
run = True
while run:
    # Set max fps: using -> tick() ->> expect #FPS
    clock.tick(fps)

    # Display Background
    display_bg()
    # Display images

    # End the game: Event
    # event.get() -> get all events
    for event in pygame.event.get():
        # EventHandlers
        if event.type == pygame.QUIT:
            # When user click's on 'X' in the top-right corner of the screen
            run = False

    # Update displays to screen!
    pygame.display.update()
# QUIT Pygame! 
pygame.quit()


 