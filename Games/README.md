# Install PyGame

## Install PyGame (Windows)

`py -m pip install -U pygame --user`

<hr>

# DevOps

## Goals / Objectives

    Goal:
    * Creating a Python game using PyGame. Why not start with an old, fancy game like Space Invaders?
    * Learn the basics of Python in a period of two weeks, through documentations and video's, able to create a functional game.
<hr>

# Pygame

`import pygame`
`from pygame.locals import *`

! Important at the end of the script, we need to quit Pygame !
`pygame.quit()`

## Initialise and display the game window

    With Pygame we can use display.set_mode(), to display the window of our game.

`screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))`
    
    Note: This will append an untitled window !

> To set a title we can use display.set_caption(), 
`pygame.display.set_caption("Name of the App")`

## Game loop
    run = True
    while run:
<hr>

## Event & EventHandlers 
    event.get() -> get all events
    for event in pygame.event.get():
        # EventHandlers
        if event.type == pygame.QUIT:
            # When user click's on 'X' in the top-right corner of the screen
            run = False
<hr>            

## Display images 

### Load an image
    using -> pygame.image.load
    
    pygame.image.load("path/to/image")

### Background image
`bg_img = pygame.image.load("./images/bg.png")`

## Display images
    Using -> screen.blit() ->> two parameters: image and coordoniates(tuppel: x and y coord.)
    def display_bg():    
        # Background image position -> take entire screen => (0,0)
        screen.blit(bg_img,(0,0))

## ! Whenever we make changes we need to update the screen
    pygame.display.update()

<hr>

## Set max. FPS

    Define fps to set a max. fps. Using clock -> pygame.time.Clock() and clock.tick()

    fps = 60 
    clock = pygame.time.Clock()
    clock.tick(fps)
<hr>






