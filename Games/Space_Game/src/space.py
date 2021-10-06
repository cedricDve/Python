import pygame
from pygame.locals import *

# Define fps and clock -> pygame.time.Clock() | To set max FPS of our Game
fps = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Create a (untitled)game-window:
    # display.set_mode() -> two parameters: width and height 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# --  Add game title: display.set_caption
pygame.display.set_caption("Space Invaders")

# Colors
red = (255,0,0)
green = (0,255,0)

# Load images: using -> pygame.image.load
bg_img = pygame.image.load("./images/bg.png")

# Display background image
# Using -> screen.blit() ->> two parameters: image and coordoniates(tuppel: x and y coord.)
def display_bg():    
    # Background image position -> take entire screen => (0,0)
    screen.blit(bg_img,(0,0))
    # Background image will be displayed as first => need to be set as a background, all other images will be displayed above!

# Create spaceship class from pygame Sprite
class Spaceship(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x,y, health):
        # inheriting the functionality of pygame Sprite class in our Spaceship class
        pygame.sprite.Sprite.__init__(self)
        # Two key-variables for Sprite: image and rect -> convert image to a rectangle
        self.image = pygame.image.load("./images/plane.png")
        # using image.get_rect()
        self.rect = self.image.get_rect()
        # Coordinates: x and y -> position our rectangle -> rect.center
        self.rect.center = [x,y]

        # Health of spaceship: spaceship start with full health (3 life-points)
        self.health_start = health
        self.health_remaining = health

        # Last shot variable = time 
        self.last_shot = pygame.time.get_ticks()

    
    # overrid update function
    def update(self):
        speed = 8
        # Cooldown variable for schooting
        # -- cooldown in mili seconds !
        cooldown = 500

        # Key press -> key.get_pressed()
        key = pygame.key.get_pressed()
        # LEFT KEY pressed
        # -- Limit to size of window => coord rect.left > 0
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        # RIGHT KEY pressed
        # -- Limit to size of window => coord rect.right < SIZE_WIDTH
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed

        # Schooting
        # Record current time -> limit # bullets in function of time !
        time_now = pygame.time.get_ticks()
        # Create bullet | time depended !
        if key[pygame.K_SPACE] and (time_now - self.last_shot) > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            # Add to bullet group => each bulet go in its own update-loop!
            bullet_group.add(bullet)
            # restatrt timer for cooldown => time = now
            self.last_shot = time_now



        # Display health bar
        # -- Draw a red rectangle, under the spaceship 
        pygame.draw.rect(screen, red , (self.rect.x,(self.rect.bottom + 10), self.rect.width, 15))
        # When health is full => display green rectangle above the red rectangle
        if self.health_remaining > 0:
            # -- width of the green rectangle should change whenever the spaceship takes dammage
            pygame.draw.rect(screen, green , (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining/self.health_start)), 15))


class Bullets(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x,y):
        # inheriting the functionality of pygame Sprite class in our Spaceship class
        pygame.sprite.Sprite.__init__(self)
        # Two key-variables for Sprite: image and rect -> convert image to a rectangle
        self.image = pygame.image.load("./images/bullet.png")
        # using image.get_rect()
        self.rect = self.image.get_rect()
        # Coordinates: x and y -> position our rectangle -> rect.center
        self.rect.center = [x,y]
    
    # overrid update function
    def update(self):
        self.rect.y -= 5
        # Remove bullets when they leave screen ! y less then 0
        if self.rect.bottom < 0:
            # Using kill ! Kill the instance: only one bullet
            self.kill()

        

# Create sprite groups -> pygame.sprite.Groups()
spaceship_group = pygame.sprite.Group()
# Bullet group
bullet_group = pygame.sprite.Group()


# Create player: instantiate spaceship
# - Center spaceship and at the bottom of the screen 
spaceship = Spaceship(int(SCREEN_WIDTH/2), SCREEN_HEIGHT - 100, 3)
# --- Add spaceship to our spaceship group
spaceship_group.add(spaceship)




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

    # Update spaceship 
    spaceship.update()
    
    # Update bulletgroup !Group
    bullet_group.update()

    # Display sprite groups: using -> draw() -> build in draw and update function of Sprite
    spaceship_group.draw(screen)
    bullet_group.draw(screen)


    # Update displays to screen!
    pygame.display.update()
# QUIT Pygame! 
pygame.quit()


 