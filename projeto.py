import pygame, sys
import pygame.freetype
import numpy as np
from pygame.math import Vector2
import random
import math

#Colors
white = (240, 240, 240)
black = (10, 10, 10)
red = (240, 10, 10)
darkred = (170, 10, 10)
pink = (240, 126, 126)
blue = (10, 10, 205)
darkblue = (10, 10, 100)
darkyellow = (170, 170, 10)
yellow = (240, 240, 10)
babyyellow = (240, 240, 120)
babypink = (240, 180, 180)
grey = (105, 105, 105)
brown = (89,59,19)
orange = (200, 120, 40)
babyblue = (135,206,250)
babygreen = (100, 250, 100)
green = (10, 250, 10)
darkgreen = (10, 170, 10)

#Variables



GRAVITY = 9.8

# Balls shown on screen
class Projectile():

    def __init__(self, x, y, v0, angle, color):

        # Physics variables
        self.x = x
        self.y = y  
        self.v0 = v0
        self.angle = angle
        self.vx = 0
        self.vy = 0
        self.mass = 1
        self.netforceY = 0
        self.accelerationY = 0
        self.netforceX = 0
        self.accelerationX = 0
        self.delta_time = 0.1
        self.time = 0

        # Display variables
        self.size = 5
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        self.color = color

        # Gameplay Variables
        self.timer = 0.5
        self.timeInBox = 0

        # Trail variables
        self.trailX = []
        self.trailY = []

        


    # Shows ball o screen
    def draw(self, screen):
        
        pygame.draw.circle(screen, black, (self.x, self.y), self.size + 1)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    # Updates ball position
    def update(self, drag):

        self.netforceY = self.mass * GRAVITY
        self.accelerationY = self.netforceY / self.mass

        self.netforceX = self.mass * drag
        self.accelerationX = self.netforceX / self.mass

        self.time += self.delta_time

        self.x += self.delta_time * self.vx + (0.5 * self.accelerationX * (self.delta_time ** 2))

        self.y += self.delta_time * self.vy - (0.5 * self.accelerationY * (self.delta_time ** 2))
        
        self.vy += self.delta_time * GRAVITY

        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    # Checks if ball collided with x
    def calculateCollisions(self, x):

        return pygame.Rect.colliderect(self.rect, x)
            

def menu():

    # Game Window Resolution
    res_x = 800
    res_y = 600

    background_x = 0

    screen = pygame.display.set_mode((res_x, res_y))

    while (True):

        mouse_pos = pygame.mouse.get_pos()

        for evt in pygame.event.get():
                        
            if evt.type == pygame.KEYDOWN:

                if evt.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()
                
            if (evt.type == pygame.MOUSEBUTTONDOWN):
                
                
                if (evt.button == 1):
                    
                    # Starts the game loop if mouse is on start button
                    if (20 <= mouse_pos[0] <= 320 and 300 <= mouse_pos[1] <= 450 ):
                    
                        gameLoop()
                    
                    # Exits the game
                    if (480 <= mouse_pos[0] <= 780 and 300 <= mouse_pos[1] <= 450 ):

                        pygame.quit()
                        sys.exit()

        # Shows menu
        screen.fill(grey)

        screen.blit(pygame.transform.scale(pygame.image.load("Background.png"), (1400, 600)), (background_x,0))
        screen.blit(pygame.transform.scale(pygame.image.load("LogoFinal.png"), (300, 300)), (250, 50))
        screen.blit(pygame.transform.scale(pygame.image.load("StartButton.png"), (300, 150)), (20, 300))
        screen.blit(pygame.transform.scale(pygame.image.load("ExitButtonNotDestroyed.png"), (300, 150)), (480, 300))

        # Moves background
        if (background_x >= -600):

            background_x -= 1
        
        else:

            background_x = 0

        pygame.display.update()



def gameLoop():

    # Tracks time since last shot
    shootingCooldown = 0

    # Saves colors to give a random color to every ball
    colors = [white, black, red, 
              pink, blue, darkblue, 
              yellow, babypink, 
              grey, brown, orange, 
              babyblue]

    # Game Window Resolution
    res_x = 800
    res_y = 600

    # Starting values for ball
    angle0 = 40
    projectileY0 = 270
    projectileX0 = 70
    v0 = 50

    screen = pygame.display.set_mode((res_x, res_y))

    # Saves time to show trail of tragectory
    test2 = 0.2

    # Wind variables
    air_density = 1.225
    drag_coefficient = 0
    windType = ""

    # Time Setup
    clock = pygame.time.Clock()


    # Font 
    my_font = pygame.freetype.Font("advanced_pixel-7.ttf", 19)

    # Checks if bar protectiong the goal is active
    protectionEnabled = True
    protectionTimer = 0

    # Initalize tragectory projectile
    projectile2 = Projectile(projectileX0, projectileY0, v0, angle0, green)
    projectile2.vx = projectile2.v0 * math.cos(math.radians(projectile2.angle))
    projectile2.vy = -projectile2.v0 * math.sin(math.radians(projectile2.angle))

    # Saves score
    score = 0

    # Saves all the balls shot
    projectiles = []

    # Resets position of chest and bouncing platform
    reset = True

    
    while (True):

        for evt in pygame.event.get():
            
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evt.type == pygame.KEYDOWN:
                

                if evt.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                # Shoot a ball
                if evt.key ==  pygame.K_SPACE and shootingCooldown == 0:
                    
                    shootingCooldown += 0.3
                    
                    projectiles.append(Projectile(projectileX0, projectileY0, v0, angle0, colors[random.randrange(0, len(colors))]))
                    projectiles[len(projectiles) - 1].vx = projectiles[len(projectiles) - 1].v0 * math.cos(math.radians(projectiles[len(projectiles) - 1].angle))
                    projectiles[len(projectiles) - 1].vy = -projectiles[len(projectiles) - 1].v0 * math.sin(math.radians(projectiles[len(projectiles) - 1].angle))

    
                
                # Change angle with up down arrows
                if evt.key == pygame.K_UP:
                    
                    
                    angle0 += 5

                if evt.key == pygame.K_DOWN:

                    
                    angle0 -= 5

                # Change power with left right arrows
                if evt.key == pygame.K_RIGHT:

                    v0 += 5

                if evt.key == pygame.K_LEFT:
                    
                    v0 -= 5

                # EVerytime a key is touched reset tragectory projectile 
                projectile2 = Projectile(projectileX0, projectileY0, v0, angle0, green)

                projectile2.vx = projectile2.v0 * math.cos(math.radians(projectile2.angle))
                projectile2.vy = -projectile2.v0 * math.sin(math.radians(projectile2.angle))

                test2 = 0.2

        # Resets the positins of the goal, platform and changes the wind strength and direction
        if (reset):

            drag_coefficient = random.randrange(0, 10)
            if(drag_coefficient == 0):
                windType = "No Wind"
            elif (1 <= drag_coefficient <= 3):
                windType = "Weak"
            elif (4 <= drag_coefficient <= 6):
                windType = "Normal"
            elif (7 <= drag_coefficient <= 10):
                windType = "Strong"

            
            drag_coefficient /=  100 * random.choice((-1, 1))

            bouncyPlatformX = 700
            bouncyPlatformY = random.randrange(100, 300)

            bouncyPlatformRect = pygame.Rect(bouncyPlatformX, bouncyPlatformY, 40, 100)

            woodBoxX = random.randrange(200, 400)
            woodBoxY = random.randrange(400, 500)
            woodBoxRect = pygame.Rect(woodBoxX, woodBoxY, 200, 80)

            woodBoxWallLeftX = woodBoxX
            woodBoxWallLeftY = woodBoxY
            woodBoxWallLeft = pygame.Rect(woodBoxWallLeftX, woodBoxWallLeftY, 20, 80)

            woodBoxWallRightX = woodBoxX + 180
            woodBoxWallRightY = woodBoxY
            woodBoxWallRight = pygame.Rect(woodBoxWallRightX, woodBoxWallRightY, 20, 80)
            woodBoxFloor = pygame.Rect(woodBoxX + 10, woodBoxY + 76, 182, 4)

            woodBoxProtectionX = woodBoxX
            woodBoxProtectionY = woodBoxY - 20
            woodBoxProtection = pygame.Rect(woodBoxProtectionX, woodBoxProtectionY, 200, 20)    

            reset = False


        # Cooldown for each shot
        if shootingCooldown >= 0.2:
            shootingCooldown += 0.3

        if (shootingCooldown >= 20):
            shootingCooldown = 0

        # Paint background grey
        screen.fill(grey)

        # Display background
        screen.blit(pygame.transform.scale(pygame.image.load("LevelExampleMatematica.png"), (1070, 600)), (0,0))

        # Displays goal
        screen.blit(pygame.image.load("BackGroundChest.png"), (woodBoxX, woodBoxY))
        screen.blit(pygame.image.load("BackChest.png"), (woodBoxX, woodBoxY))
        
        screen.blit(pygame.image.load("Borracha.png"), (bouncyPlatformX, bouncyPlatformY))



        # Initalizes drag 
        drag = -0.5 * drag_coefficient * air_density *  (projectile2.size / 4)
        

        # Updates tragectory ball
        projectile2.update(0)

        if (projectile2.time > test2 and test2 < 3):
            test2 += 0.5
            projectile2.trailX.append(projectile2.x)
            projectile2.trailY.append(projectile2.y)

        # Show trail on screen
        for i in range(len(projectile2.trailX)):
            pygame.draw.circle(screen, black, (projectile2.trailX[i], projectile2.trailY[i]), 3)
            pygame.draw.circle(screen, projectile2.color, (projectile2.trailX[i], projectile2.trailY[i]), 2)

        

        
        # Timer for protection to be disabled
        if(not protectionEnabled):

            protectionTimer += 0.3

        if(protectionTimer >= 30):

            protectionEnabled = True
            protectionTimer = 0


        # Updates every projectile on screen and checks for collisions
        for projectile in projectiles:

            drag = -0.5 * drag_coefficient * air_density * (projectile.vx ** 2) * (projectile.size / 4)

            print(drag)

            projectile.update(drag)

            # COLLISIONS
            if(projectile.calculateCollisions(bouncyPlatformRect)):
                
                pop.play()
                if (bouncyPlatformX + projectile.size * 2 < projectile.x < bouncyPlatformX + 40):
                    projectile.vy *= -1

                if (projectile.y > bouncyPlatformY):
                    projectile.vx *= -1

                protectionEnabled = False
                
            if(projectile.calculateCollisions(woodBoxWallLeft)):
                
                pop.play()
                if (woodBoxWallLeftX > projectile.x > woodBoxWallLeftX):
                    projectile.vy *= -1

                if (projectile.y > woodBoxWallLeftY + projectile.size * 2):
                    projectile.vx *= -1

            if(projectile.calculateCollisions(woodBoxWallRight)):

                pop.play()
                if (woodBoxWallRightX > projectile.x > woodBoxWallRightX):
                    projectile.vy *= -1

                if (projectile.y > woodBoxWallRightY + projectile.size * 2):
                    projectile.vx *= -1

            if(projectile.calculateCollisions(woodBoxFloor)):

                projectile.vy *= -0.5

            if(projectile.calculateCollisions(woodBoxRect)):
                
                drag = 0
                projectile.timeInBox += 0.3
            
            if (protectionEnabled):
                if(projectile.calculateCollisions(woodBoxProtection)):

                    pop.play()
                    if (woodBoxProtectionX + 200 > projectile.x > woodBoxProtectionX):
                        projectile.vy *= -1

                    if (projectile.y > woodBoxProtectionY + projectile.size * 2):
                        projectile.vx *= -1
            
            
            # Save the ball position every second to do the trail
            if (projectile.time > projectile.timer):
                projectile.timer += 0.3
                projectile.trailX.append(projectile.x)
                projectile.trailY.append(projectile.y)
            
            if projectile.y > res_y:
                projectile.trailX = []
                projectile.trailY = []

            # Show trail on screen
            for i in range(len(projectile.trailX)):
                pygame.draw.circle(screen, black, (projectile.trailX[i], projectile.trailY[i]), 3)
                pygame.draw.circle(screen, projectile.color, (projectile.trailX[i], projectile.trailY[i]), 2)

            # Show ball on screen
            projectile.draw(screen)

            # Checks if ball was on goal for a timer, and gives score
            if(projectile.timeInBox >= 20):
                
                yay.play()
                score += 1
                protectionEnabled = True
                protectionTimer = 0
                reset = True
                projectiles.remove(projectile)

        # DIplays front of the goal
        screen.blit(pygame.image.load("FrontChest.png"), (woodBoxX, woodBoxY))

        # Displays board protection
        if (protectionEnabled):
            screen.blit(pygame.image.load("Board.png"), (woodBoxProtectionX, woodBoxProtectionY))

        # Displays score and wind strength
        my_font.render_to(screen, (650, 20), "Score: " + str(score), black, size = 40)
        my_font.render_to(screen, (650, 60), "Wind: ", black, size = 40)


        if (windType == "No Wind"):
            my_font.render_to(screen, (710, 60), windType, black, size = 40)
        elif (windType == "Weak"):
            my_font.render_to(screen, (710, 60), windType, darkgreen, size = 40)
        elif (windType == "Normal"):
            my_font.render_to(screen, (710, 60), windType, darkyellow, size = 40)
        elif (windType == "Strong"):
            my_font.render_to(screen, (710, 60), windType, darkred, size = 40)
        
        if (drag_coefficient > 0):
            screen.blit(pygame.transform.scale(pygame.image.load("leftArrow.png"), (68, 40)), (710, 85))
        if (drag_coefficient < 0):
            screen.blit(pygame.transform.scale(pygame.image.load("rightArrow.png"), (68, 40)), (710, 85))

        pygame.display.update()

        clock.tick(60)
          
# Controls the game
def main():

    pygame.init()

    #The background music
    pygame.mixer.init()
    music = pygame.mixer.Sound("music.mp3")
    music.set_volume(0.1)
    music.play(-1)

    #The sound when clicking 
    global pop
    pop = pygame.mixer.Sound("pop.wav")
    pop.set_volume(0.05)

    #The sound of coins, opens backpack
    global yay
    yay = pygame.mixer.Sound("yay.wav")
    yay.set_volume(0.5)

    # Shows the menu
    menu()

    


main()