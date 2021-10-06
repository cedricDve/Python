import pygame

# init pygame

pygame.init()

# Game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Castle Defender XI")

# Load images
# -- Background image
bg_img = pygame.image.load('./images/bg.png')
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
castle_img_100 = pygame.image.load('./images/castle1.png')

# FPS
clock = pygame.time.Clock()
FPS =60

class Castle():
    # Cunstructor
    def __init__(self, image100, x,y, scale):
        self.health = 1000
        self.max_health = self.health
        width = image100.get_width()
        height = image100.get_height()
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.image = self.image100
        # X en Y coordinates already passed in constructor
        screen.blit(self.image, self.rect )

# Create castle
# -- size  65% of orginal with 
castle = Castle(castle_img_100, SCREEN_WIDTH - 220 , SCREEN_HEIGHT - 300, 0.65)

# Game loop
run = True
while run:

    # Set FPS
    clock.tick(FPS)

    # Display background images
    screen.blit(bg_img, (0,0))

    # Draw castle
    castle.draw()
   

    #Event Handler: QUIT game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Game when user click on 'X' (top-right-corner)
            run = False

    # Update display
    pygame.display.update()

pygame.quit()


