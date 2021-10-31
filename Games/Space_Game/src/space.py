import pygame
from pygame import mixer # for audio
from pygame.locals import *
import random
import pymysql.cursors # Add pymsql.cursor -> connected to mysql running in docker-container
import bcrypt # encrypt password
import cryptography # for sha256
import keyboard # python keyboard event

# Login variable
logged_in = False

# Init Pygame-font
pygame.font.init()
# Init mixer => to load soundeffects
pygame.mixer.pre_init(44100, -16, 2, 512) # to handle sound latency
mixer.init()

# Define FPS and clock -> pygame.time.Clock() | To set max FPS of our Game
FPS = 60
clock = pygame.time.Clock()

# Screen variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
# Create screen : create a (untitled)game-window:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))# display.set_mode() -> two parameters: width and height 
# --  Add game title: display.set_caption
pygame.display.set_caption("Space Invaders")

# Define fonts
font30 = pygame.font.SysFont('Arial', 30)
font40 = pygame.font.SysFont('Arial', 40)
smallfont = pygame.font.SysFont('Corbel',35)

# Load sound: soundeffects
explosion_sound_effect = pygame.mixer.Sound("./sounds/dead.wav")
explosion_sound_effect.set_volume(0.25)
explosion2_sound_effect = pygame.mixer.Sound("./sounds/explosion.wav")
explosion2_sound_effect.set_volume(0.15)
dead_sound_effect = pygame.mixer.Sound("./sounds/impact.wav")
dead_sound_effect.set_volume(0.25)
shoot_sound_effect =  pygame.mixer.Sound("./sounds/shoot.wav")
shoot_sound_effect.set_volume(0.25)

# Game variables
level = 1
score = 0
# -- rows and cols for Aliens
rows = 2
cols = 2
# -- Alien cooldown
alien_cooldown = 500 # in MS
last_alien_shot = pygame.time.get_ticks() # initialized when game starts
# -- Countdown for text
countdown  = 3 # represent secs
last_count = pygame.time.get_ticks()
# -- Game Over
game_over = 0 # 0 = NO game over | 1 = player has WON | -1 = GAME OVER
extra_life_point = 0 

# Colors
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)

#Database connection
db_connection = pymysql.connect(host='localhost',
                             user='root',
                             password='p@ssw0rd1',
                             database='spaceGame',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# Database function Register                          
def register():
    register = False
    while register == False:
        print("Please answer to the following questions:")
        name = input("Your name: ")
        email = input("Your email: ")
        psw = input("Your password: ")
        repeat_psw = input("Repeat your password: ")
        if(psw == repeat_psw):            
            password = psw.encode('utf-8')
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
            with db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
                db_connection.commit()
                register = True
        else:
            print("Error, password must be the same twice")
           
# Database function Login
def login():
    global logged_in
    while logged_in == False:        
        email = input("Your email: ")
        psw = input("Your password: ")
        password = psw.encode('utf-8')
        with db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
                user = cursor.fetchone()
                if (user != None):
                    if len(user) > 0:
                        if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                            print("Logged in successfully")
                            logged_in = True
                        else:
                            print("Error password and email not match")
                    else:
                        print("Error user not found")

# Load images: using -> pygame.image.load
bg_img = pygame.image.load("./images/bg.png")

# Display background image

def display_bg():    
    # Background image position -> take entire screen => (0,0)
    screen.blit(bg_img,(0,0))# Using -> screen.blit() ->> two parameters: image and coordoniates(tuppel: x and y coord.)
    # Background image will be displayed as first => need to be set as a background, all other images will be displayed above!

# Creating text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    # Blit the image to the screen
    screen.blit(img, (x,y))
# Create spaceship class from pygame Sprite
class Spaceship(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x, y, health):
        # inheriting the functionality of pygame Sprite class in our Spaceship class
        pygame.sprite.Sprite.__init__(self)
         # Two key-variables for Sprite: image and rect -> convert image to a rectangle
        img = pygame.image.load("./images/plane.png")
        self.image = pygame.transform.scale(img, (80, 100))
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

        game_over = 0

        if(score >= 500):           
            img = pygame.image.load("./images/plane-1.png")
            self.image = pygame.transform.scale(img, (80, 100))
        elif(score >= 1000):
            img = pygame.image.load("./images/plane-2.png")
            self.image = pygame.transform.scale(img, (80, 100))

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
            # Sound effect
            shoot_sound_effect.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            # Add to bullet group => each bulet go in its own update-loop!
            bullet_group.add(bullet)
            # restatrt timer for cooldown => time = now
            self.last_shot = time_now

        # Update mask   
        # -- Able to create an image with and ignore the transparant pixels" => use mask
        self.mask = pygame.mask.from_surface(self.image)



        # Display health bar
        # -- Draw a red rectangle, under the spaceship 
        pygame.draw.rect(screen, red , (self.rect.x,(self.rect.bottom + 10), self.rect.width, 15))
        # When health is full => display green rectangle above the red rectangle
        if self.health_remaining > 0:
            # -- width of the green rectangle should change whenever the spaceship takes dammage
            pygame.draw.rect(screen, green , (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining/self.health_start)), 15))
        # When no health left => big explosion animation
        elif self.health_remaining <= 0:
            # Sound effect
            dead_sound_effect.play()
            # Explosion animation
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            # Game over
            game_over = -1
        return game_over


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
        # Check if bullet is in contact with an alien group
        if pygame.sprite.spritecollide(self, alien_group, True): # when collision of self(Bullet) with an alien (in alien_group), True => do_kill (kill the alien)
            # When bullet kills an alien => kill bullet !!
            self.kill()
            # Sound effect
            explosion_sound_effect.play()
            # Explosion animation
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)

            # Add 100 to score            
            global score
            score = score + 100
            info_score()
           


# Aliens
class Aliens(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x,y):
        # inheriting the functionality of pygame Sprite class in our Spaceship class
        pygame.sprite.Sprite.__init__(self)
        # Get random images from our images file -> using random: import random
        image = pygame.image.load("./images/alien-" + str(random.randint(1,3)) + ".png")
        self.image = pygame.transform.scale(image, (int((SCREEN_WIDTH -300)/cols ), int((SCREEN_HEIGHT -300) / rows)))
        # using image.get_rect()
        self.rect = self.image.get_rect()
        # Coordinates: x and y -> position our rectangle -> rect.center
        self.rect.center = [x,y]
        self.move_counter = 0
        # Direction + right - left
        self.move_direction = 1

    def update(self):
        # Let aliens move from right to the left
        self.rect.x += self.move_direction
        self.move_counter += 1
        # ABS(counter) => 1 or -1  
        if abs(self.move_counter) > 75:
            # Flip movement direction ! 
            self.move_direction *= -1
            # Flip move_counter !
            self.move_counter *= self.move_direction

class Alien_Bullets(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x,y):
        # inheriting the functionality of pygame Sprite class in our Spaceship class
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("./images/alien_bullet.png")
        self.image = pygame.transform.scale(image, (20,40))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    
    # overrid update function
    def update(self):
        # Alien_bullets go down 
        self.rect.y += 2
        # Remove Alien_bullets when they leave screen ! y greater then sceen-height
        if self.rect.top > SCREEN_HEIGHT:
            # Using kill ! Kill the instance: only one bullet
            self.kill()
        # Whenever an alien shoots -> only touch the spaceship and not the transperant pixels => mask
        # -- pygame.sprite.collide_mask => mask collision
        if pygame.sprite.spritecollide(self, spaceship_group , False, pygame.sprite.collide_mask):
            self.kill()
            # Sound effect
            explosion2_sound_effect.play()
            # When alien bullet touchs spaceship => kill alien_bullet 
            # And reduce spaceship health
            spaceship.health_remaining -= 1
             # Explosion animation
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)

# Create Explosion class
class Explosion(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x,y, size): # size to adjust size of explosion
        # inheriting the functionality of pygame Sprite class in our Spaceship class
        pygame.sprite.Sprite.__init__(self)
        # List of images => for animation
        self.images = []
        for num in range(1,6):
            image = pygame.image.load(f"./images/explosion{num}.png")
            # Scale images based on size
            if size == 1:
                image = pygame.transform.scale(image, (20,20))
            if size == 2:
                image = pygame.transform.scale(image, (40,40))
            if size == 3:
                image = pygame.transform.scale(image, (150,150))
            # Add image to list of images
            self.images.append(image)
        # index(track witch explosion img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        # counter => control the speed of animation
        self.counter = 0
    
    def update(self):
        explosion_speed = 3
        # Update explosion animation => counter++
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1 :
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        # End the animation when completed
        if self.index >= len(self.images) -1  and self.counter >= explosion_speed:
            # Kill the animation
            self.kill()        


# Info Game
def info_level():
    draw_text(f'Level:{level}', font30, white, int(SCREEN_WIDTH - 150) ,int( 10))

def info_score():
    draw_text(f'Score:{score}', font30, white, int(SCREEN_WIDTH - 150) ,int( 40))

# Create Sprite Groups -> pygame.sprite.Groups()
# -- Spaceship Group
spaceship_group = pygame.sprite.Group()
# -- Bullet Group
bullet_group = pygame.sprite.Group()
# -- Alien group 
alien_group = pygame.sprite.Group()
# -- Alien_Bullet Group 
alien_bullet_group = pygame.sprite.Group()
# -- Explosion Group
explosion_group = pygame.sprite.Group()

# Create Aliens
def create_aliens():
    # Creating aliens depending on witch row and col positioned
    for row in range(rows):
        for item in range(cols):
            # Aliens spaced by 100 px 
            alien = Aliens(100+ item * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()

# Create player: instantiate spaceship
spaceship = Spaceship(int(SCREEN_WIDTH/2), SCREEN_HEIGHT - 100, 3)# Center spaceship and at the bottom of the screen 
spaceship_group.add(spaceship)# - Add spaceship to our spaceship group

def game_over_text():
    draw_text('GAME OVER!', font40, red, int(SCREEN_WIDTH/2 -100) ,int( SCREEN_HEIGHT/2 ))
    draw_text('Play Again?', font40, white, int(SCREEN_WIDTH/2 - 100) ,int( SCREEN_HEIGHT/2 + 40))
    draw_text('YES(Y) or NO(N)', font40, white, int(SCREEN_WIDTH/2 - 100) ,int( SCREEN_HEIGHT/2 + 80))



# Authentication 
# -- Before the game starts a user need to authenticate
print("Please login to be able to save you points: \n Press (x) to login  \n Press (y) to register \n ")
# Login
if keyboard.read_key() == "x":
    print("Login")
    login() 
# Register 
if keyboard.read_key() == "y":
    print("Register")
    register()
    print("You are now ready to go !")
    print("The game will start .. NOW")
    
# Game loop: game will run until 'run != true'
run = True
while run:
    # Set max FPS: using -> tick() -> expect #FPS
    clock.tick(FPS)
    # Display Background
    display_bg()

    # Countdown before game starts
    if countdown == 0:
        info_level()
        info_score()
        # Create random alien_bullets -> based in a timer
        # record current time
        time_now = pygame.time.get_ticks()
        # Alien shoot
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0: 
        # After one second fire a bullet and no more then 5 bullets created (until a alien_bullet reachs the bottom of the screen!
            # Fire a bullet 
            # -- Choose alien: picking a random alien from alien_groups.sprites
            attacking_alien = random.choice(alien_group.sprites())
            # -- Generate a bullet under the alien
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            # Reset timer
            last_alien_shot = time_now

        # If aliens have been killed
        if len(alien_group) == 0:
            # User has won
            game_over = 1
        # Update only if game is not over
        if game_over == 0:
            # Update spaceship 
            game_over = spaceship.update()            
            # Update Sprite Groups           
            bullet_group.update()# -- Spaceship bullet
            # -- Aliens
            alien_group.update()
            alien_bullet_group.update()
        else:
            if game_over == -1:# Game over
                if extra_life_point == 0:
                    draw_text('One last life-point ?', font40, white, int(SCREEN_WIDTH/2 - 110) ,int( SCREEN_HEIGHT/2 + 60))
                    draw_text('YES(Y) or NO(N)', font40, white, int(SCREEN_WIDTH/2 - 110) ,int( SCREEN_HEIGHT/2 + 100))
                    key = pygame.key.get_pressed()

                    if key[pygame.K_y]:             
                        game_over = 0
                        extra_life_point = 1
                        spaceship.health_remaining = 1        
                    elif key[pygame.K_n]:
                        game_over_text()
                        key = pygame.key.get_pressed()

                        if key[pygame.K_y]:  
                            # restart game 
                            game_over = 0
                            countdown = 0
                            extra_life_point = 0 
                            spaceship.health_remaining = spaceship.health_start
                            alien_group.empty()
                            alien_bullet_group.empty()
                            create_aliens()
                            level = 1
                            score = 0
                            rows = 2
                            cols = 2                            
                            
                        elif key[pygame.K_n]:
                            run = False  
                else:
                    game_over_text()
                    key = pygame.key.get_pressed()
                    if key[pygame.K_y]:  
                        # restart game 
                        game_over = 0
                        countdown = 0
                        extra_life_point = 0 
                        spaceship.health_remaining = spaceship.health_start
                        alien_group.empty()
                        alien_bullet_group.empty()
                        create_aliens()
                        level = 1
                        score = 0
                        rows = 2
                        cols = 2

                    elif key[pygame.K_n]:
                        run = False 
            if game_over == 1:#Game won
             
               
                draw_text('LEVEL WON!', font40, green, int(SCREEN_WIDTH/2 -100) ,int( SCREEN_HEIGHT/2))
                draw_text('Continue to next level?', font40, white, int(SCREEN_WIDTH/2 - 130) ,int( SCREEN_HEIGHT/2 + 40))
                draw_text('YES(Y) or NO(N)', font40, white, int(SCREEN_WIDTH/2 - 120) ,int( SCREEN_HEIGHT/2 + 80))
                key = pygame.key.get_pressed()
                if key[pygame.K_y]:  
                    level = level +1 
                    if(level <= 3):
                        rows = rows +1 
                        cols = cols +1
                    elif(level <= 10):
                       alien_cooldown = alien_cooldown - 200 # in MS
                    elif(level <= 12):
                        rows = rows +1 
                        cols = cols +1
                    elif(level <= 20):
                       alien_cooldown = alien_cooldown - 25 # in MS
                    # restart game 
                    game_over = 0
                    countdown = 0
                    alien_group.empty()
                    create_aliens()

                elif key[pygame.K_n]:
                    run = False 
                

                                   
    if countdown > 0:
        draw_text('GET READY!', font40, white, int(SCREEN_WIDTH/2 -110) ,int( SCREEN_HEIGHT/2 ))
        draw_text(str(countdown), font40, red , int(SCREEN_WIDTH/2 -10) ,int( SCREEN_HEIGHT/2 + 40))
       
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000: # 1second past
            countdown -= 1
            # Reset timer 
            last_count = count_timer

    # -- Explosion Group
    explosion_group.update()
 
    # Draw Sprite Groups
    # -- Display sprite groups: using -> draw() -> build in draw and update function of Sprite
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)


    # End the game: Event
    # -- event.get() -> get all events
    for event in pygame.event.get():
        # EventHandlers
        if event.type == pygame.QUIT:
            # When user click's on 'X' in the top-right corner of the screen
            run = False 
            
    # Update displays to screen!
    pygame.display.update()
# QUIT Pygame! 
pygame.quit()