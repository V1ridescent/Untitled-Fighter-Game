import pygame
import pygame.font
import sys
import os

#Init
pygame.init()
clock = pygame.time.Clock()
screen_width = 1456
screen_height = 816
screen = pygame.display.set_mode((screen_width, screen_height))
background_image = pygame.image.load('scene/background.png')
ground = pygame.image.load('scene/ground.png')
scale_factor = 0.7
scaled_background = pygame.transform.scale(background_image, (int(background_image.get_width() * scale_factor), int(background_image.get_height() * scale_factor)))
pygame.display.set_caption('Fighter Game - Justin Jaques')


#Getting Font
font_path = os.path.abspath('font/mainfont.TTF')
font_size = 30
main_font = pygame.font.Font(font_path, font_size)
beta_text = 'Untitled Fighter Game Early Alpha' 
name_text = 'Developed by Justin Jaques'
text_render = main_font.render(beta_text, True, (255, 255, 255))
text1_render = main_font.render(name_text, True, (255, 255, 255))


# Player 1 Animation List
p1_animation_list_idle = [
    'player1_animation/idle0.png', 
    'player1_animation/idle1.png', 
    'player1s_animation/idle2.png', 
    'player1_animation/idle3.png'
]
p1_animation_idle_steps = 4 



#Player 1 Class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.speed = 5
        self.is_attacking = False
        self.health = 100;
        self.attack_cooldown = 0  # Initial cooldown timer
        self.attack_delay = 500  # Cooldown duration in milliseconds
        self.isIdle = True;
        self.isRunning = False

    def draw(self, surface):
        hitbox_p1 = pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 50, 100))

   
    def attack(self, surface):
        if self.is_attacking and self.attack_cooldown <= 0:  # Check if not in cooldown
            attack_box_p1 = pygame.draw.rect(surface, (255, 0, 0), (self.x + 50, self.y, 100, 50))
            self.attack_cooldown = self.attack_delay  # Set cooldown timer      

    def update(self, events):
        self.attack_cooldown -= clock.get_time()  # Decrement cooldown timer
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.xVel = -self.speed
                    self.isRunning = True
                elif event.key == pygame.K_RIGHT:
                    self.xVel = self.speed
                    self.isRunning = True
                elif event.key == pygame.K_SPACE:  # Start attacking when space key is pressed
                    self.is_attacking = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.xVel = 0
                elif event.key == pygame.K_SPACE:  # Stop attacking when space key is released
                    self.is_attacking = False
            else:
                self.idle = True
        self.x += self.xVel

        
    def draw_health_bar(self, surface):
        # Draw the outline of the health bar
        pygame.draw.rect(surface, (255, 0, 0), (self.x - 25, self.y - 20, 100, 10))
        # Calculate the width of the health bar based on the player's health
        health_width = (self.health / 100) * 100
        # Draw the health bar
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 25, self.y - 20, health_width, 10))

#Player 2 Class
class Player2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.speed = 5
        self.is_attacking = False
        self.health = 100;  
        self.attack_cooldown = 0  # Initial cooldown timer
        self.attack_delay = 500  # Cooldown duration in milliseconds

    def draw(self, surface):
        hitbox_p2 = pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 50, 100))
   
    def attack(self, surface):
        if self.is_attacking and self.attack_cooldown <= 0:
            attack_box_p2 = pygame.draw.rect(surface, (255, 0, 0), (self.x - 100, self.y, 100, 50))
            self.attack_cooldown = self.attack_delay
            
    def update(self, events):
        self.attack_cooldown -= clock.get_time()  # Decrement cooldown timer
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.xVel = -self.speed
                elif event.key == pygame.K_d:
                    self.xVel = self.speed
                elif event.key == pygame.K_f:  # Start attacking when space key is pressed
                    self.is_attacking = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.xVel = 0
                elif event.key == pygame.K_f:  # Stop attacking when space key is released
                    self.is_attacking = False
        self.x += self.xVel

    def draw_health_bar(self, surface):
        # Draw the outline of the health bar
        pygame.draw.rect(surface, (255, 0, 0), (self.x - 25, self.y - 20, 100, 10))
        # Calculate the width of the health bar based on the player's health
        health_width = (self.health / 100) * 100
        # Draw the health bar
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 25, self.y - 20, health_width, 10))


def check_collision():
    if player1.is_attacking and player2.x < player1.x + 150 and player2.x + 50 > player1.x + 50 and player1.y < player2.y + 100 and player1.y + 100 > player2.y:
        player2.health -= .05  # Deduct health if there's a collision

    # Check for collision between player 2's attack box and player 1's hit box
    if player2.is_attacking and player1.x < player2.x + 100 and player1.x + 50 > player2.x - 100 and player1.y < player2.y + 100 and player1.y + 100 > player2.y:
        player1.health -= .05



player1 = Player(100, 650)
player2 = Player2(300, 650)

#Game Loop
while True:
    clock.tick(100)
    screen.blit(scaled_background, (0, 0))
    screen.blit(ground, (0, 750))
    events = pygame.event.get()  # Move this line inside the loop to update events continuously
    screen.blit(text_render, (screen_width // 5.5 - text_render.get_width() // 2, screen_height // 50 - text_render.get_height() // 2))
    screen.blit(text1_render, (screen_width // 5.5 - text_render.get_width() // 2, screen_height // 34 - text_render.get_height() // 900))

    player1.update(events)
    player1.draw(screen)
    player1.attack(screen)
    player1.draw_health_bar(screen)

    player2.update(events)
    player2.draw(screen)
    player2.attack(screen)
    check_collision()
    player2.draw_health_bar(screen)
    

    pygame.display.update()