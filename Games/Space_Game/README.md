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

## Add music using mixer
`from pygame import mixer`

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


https://www.youtube.com/watch?v=bFn1XrtRnn8&ab_channel=CodingWithRuss




Alien shooting bullets
1. Choose Alien that will shoot
=> To create random alien_bullets -> based in a timer

Colisions spaceship bullet with aliens
Count down before game starts
In pygame we cant display text - like a string
We need to convert our string into an image before !

# init font from pygamee.font -> otherwise error!
pygame.font.init()
We need a font, a color then we can render the font as an image



## Mouse event

  for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:         
            #Click on Quit
            if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2+140 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:
                register()


      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2+140 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:
        pygame.draw.rect(screen,color_light,[SCREEN_WIDTH/2,SCREEN_HEIGHT/2,140,40])
          
    else:
        pygame.draw.rect(screen,color_dark,[SCREEN_WIDTH/2,SCREEN_HEIGHT/2,140,40])
      
    # superimposing the text onto our button
    screen.blit(text , (SCREEN_WIDTH/2+50,SCREEN_HEIGHT/2))