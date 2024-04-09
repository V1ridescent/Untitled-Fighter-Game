# Import necessary libraries
import pygame
import pygame.font
import sys
import os
import time

# Initialize pygame
pygame.init()

# Set up the clock
clock = pygame.time.Clock()

# Screen dimensions
screen_width = 1456
screen_height = 816

# Create the display window
screen = pygame.display.set_mode((screen_width, screen_height))

# Load background image
background_image = pygame.image.load('scene/background.png')
ground = pygame.image.load('scene/ground.png')

# Scale factor for background
scale_factor = 0.7
scaled_background = pygame.transform.scale(background_image, (int(background_image.get_width() * scale_factor), int(background_image.get_height() * scale_factor)))

# Set the window caption
pygame.display.set_caption('Fighter Game - Justin Jaques')

# Load main menu and about images
main_menu_image = pygame.image.load('mainmenu/mainmenubackground.png')
about_image = pygame.image.load('mainmenu/about.png')

# Load win screens
player1_win_screen = pygame.image.load('win/player1_win.png')
player2_win_screen = pygame.image.load('win/player2_win.png')

# Path to main font
font_path = os.path.abspath('font/mainfont.TTF')

# Font size
font_size = 30

# Load main font
main_font = pygame.font.Font(font_path, font_size)

# Texts
beta_text = 'Untitled Fighter Game Early Alpha' 
name_text = 'Developed by Justin Jaques'
text_render = main_font.render(beta_text, True, (255, 255, 255))
text1_render = main_font.render(name_text, True, (255, 255, 255))

# Player texture scaling
player_texture_scale_width = 150
player_texture_scale_height = 150

player2_texture_scale_width = 150
player2_texture_scale_height = 150

# Button surface
button_surface = pygame.Surface((1456, 816))

# State system
state = [
    'Main Menu',
    'Game',
    'About',
    'Exit',
    'Player1 Win',
    'Player2 Win'
]

currentState = state[0]


# Player 1 Class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.speed = 5
        self.is_attacking = False
        self.health = 100
        self.attack_cooldown = 0  # Initial cooldown timer
        self.attack_delay = 500  # Cooldown duration in milliseconds
        self.isIdle = True
        self.animation_timer = 0  # Timer for idle animation
        self.animation_duration = 100  # Duration between idle animation frames
        self.attack_animation_duration = 50
        self.idle_animation_index = 0
        self.running_animation_index = 0
        self.attacking_animation_index = 0
        self.isRunningRight = False
        self.isRunningLeft = False
        self.isInCooldown = False
        self.canAttack = True
        self.hitbox_surface = pygame.Surface((50, 100))  # Create a surface for hitbox
        self.idle_animation_frames = [
            pygame.transform.scale(pygame.image.load(f'player1_animation/idle{i}.png'), (player_texture_scale_width, player_texture_scale_height))
            for i in range(4)
        ]

        self.running_animation_frames = [
            pygame.transform.scale(pygame.image.load(f'player1_animation/run{i}.png'), (player_texture_scale_width, player_texture_scale_height))
            for i in range(6)
        ]

        self.attacking_animation_frames = [
            pygame.transform.scale(pygame.image.load(f'player1_animation/attack{i}.png'), (player_texture_scale_width, player_texture_scale_height))
            for i in range(6)
        ]

   
    def check_attack(self, surface):
        if self.is_attacking and self.attack_cooldown <= 0:
            # Draw attack hitbox
            attack_box_p1 = pygame.draw.rect(self.hitbox_surface, (255, 0, 0), (self.x + 50, self.y, 100, 50))
            self.isIdle = False  # Player is not idle when attacking
        else:
            self.is_attacking = False
          

    def update(self, events):
        self.attack_cooldown -= clock.get_time()  # Decrement cooldown timer
        self.check_attack(screen)
        self.draw_health_bar(screen)

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.xVel = -self.speed
                    self.isIdle = False
                    self.is_attacking = False
                    self.isRunningLeft = True
                elif event.key == pygame.K_RIGHT:
                    self.xVel = self.speed
                    self.isIdle = False
                    self.is_attacking = False
                    self.isRunningRight = True
                elif event.key == pygame.K_SPACE:  # Start attacking when space key is pressed and not attacking
                    self.is_attacking = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.xVel = 0
                    self.isRunningLeft = False
                    self.isIdle = True
                elif event.key == pygame.K_RIGHT:
                    self.xVel = 0
                    self.isRunningRight = False
                    self.isIdle = True

        # Reset movement animation index and timer if not moving
        if self.isIdle:
            self.animation_timer += clock.get_time()
            if self.animation_timer >= self.animation_duration:
                self.idle_animation_index = (self.idle_animation_index + 1) % len(self.idle_animation_frames)
                self.animation_timer = 0
        elif self.isRunningRight or self.isRunningLeft:
            self.animation_timer += clock.get_time()
            if self.animation_timer >= self.animation_duration:
                self.running_animation_index = (self.running_animation_index + 1) % len(self.running_animation_frames)
                self.animation_timer = 0

        # Handle attack animation
        if self.is_attacking:
            self.animation_timer += clock.get_time()
            if self.animation_timer >= self.attack_animation_duration:
                self.attacking_animation_index = (self.attacking_animation_index + 1) % len(self.attacking_animation_frames)
                self.animation_timer = 0
                # Reset attack animation and cooldown when animation ends
                if self.attacking_animation_index == 0:
                    self.is_attacking = False
                    self.isIdle = True
                    self.attack_cooldown = self.attack_delay

        # Update position based on velocity
        self.x += self.xVel

        # Draw the appropriate animation frame based on player's state
        current_frame = None
        if self.isIdle:
            current_frame = self.idle_animation_frames[self.idle_animation_index]
        elif self.isRunningRight:
            current_frame = self.running_animation_frames[self.running_animation_index]
        elif self.isRunningLeft:
            current_frame = pygame.transform.flip(self.running_animation_frames[self.running_animation_index], True, False)
        elif self.is_attacking:
            current_frame = self.attacking_animation_frames[self.attacking_animation_index]

        if current_frame is not None:
            screen.blit(current_frame, (self.x - 50, self.y - 45))

        if self.x <= 0:
            self.x = 0
        if self.x >= 1415:
            self.x = 1415
                

    def draw_health_bar(self, surface):
        # Draw the outline of the health bar with a slight gradient effect
        pygame.draw.rect(surface, (100, 100, 100), (self.x - 26, self.y - 26, 102, 12))
        pygame.draw.rect(surface, (50, 50, 50), (self.x - 25, self.y - 25, 100, 10))

        # Calculate the width of the health bar based on the player's health
        health_width = int((self.health / 100) * 100)

        # Draw the health bar with a gradient effect
        health_color = (min(255, 255 - (self.health * 2.5)), max(0, self.health * 2.5), 0)
        pygame.draw.rect(surface, health_color, (self.x - 25, self.y - 25, health_width, 10))


# Player 2 Class
class Player2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.speed = 5
        self.is_attacking = False
        self.health = 100
        self.attack_cooldown = 0  # Initial cooldown timer
        self.attack_delay = 500  # Cooldown duration in milliseconds
        self.isIdle = True
        self.animation_timer = 0  # Timer for idle animation
        self.animation_duration = 100  # Duration between idle animation frames
        self.attack_animation_duration = 50
        self.idle_animation_index = 0
        self.running_animation_index = 0
        self.attacking_animation_index = 0
        self.isRunningRight = False
        self.isRunningLeft = False
        self.isInCooldown = False
        self.canAttack = True
        self.hitbox_surface = pygame.Surface((50, 100))  # Create a surface for hitbox
        self.idle_animation_frames = [
            pygame.transform.scale(pygame.image.load(f'player2_animation/idle{i}.png'), (player2_texture_scale_width, player2_texture_scale_height))
            for i in range(1, 9)
        ]

        self.running_animation_frames = [
            pygame.transform.scale(pygame.image.load(f'player2_animation/walk{i}.png'), (player2_texture_scale_width, player2_texture_scale_height))
            for i in range(1, 9)
        ]

        self.attacking_animation_frames = [
            pygame.transform.scale(pygame.image.load(f'player2_animation/attack{i}.png'), (player2_texture_scale_width, player2_texture_scale_height))
            for i in range(1, 11)
        ]

   
    def check_attack(self, surface):
        if self.is_attacking and self.attack_cooldown <= 0:
            # Draw attack hitbox
            attack_box_p2 = pygame.draw.rect(self.hitbox_surface, (255, 0, 0), (self.x + 50, self.y, 100, 50))
            self.isIdle = False  # Player is not idle when attacking

        else:
            self.is_attacking = False

    def update(self, events):
        self.attack_cooldown -= clock.get_time()  # Decrement cooldown timer
        self.check_attack(screen)
        self.draw_health_bar(screen)

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.xVel = -self.speed
                    self.isIdle = False
                    self.is_attacking = False
                    self.isRunningRight = False
                    self.isRunningLeft = True
                elif event.key == pygame.K_d:
                    self.xVel = self.speed
                    self.isIdle = False
                    self.is_attacking = False
                    self.isRunningLeft = False
                    self.isRunningRight = True
                elif event.key == pygame.K_f:  # Start attacking when space key is pressed and not attacking
                    self.is_attacking = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.xVel = 0
                    self.isRunningLeft = False
                    self.isIdle = True
                elif event.key == pygame.K_d:
                    self.xVel = 0
                    self.isRunningRight = False
                    self.isIdle = True

        # Reset movement animation index and timer if not moving
        if self.isIdle:
            self.animation_timer += clock.get_time()
            if self.animation_timer >= self.animation_duration:
                self.idle_animation_index = (self.idle_animation_index + 1) % len(self.idle_animation_frames)
                self.animation_timer = 0
        elif self.isRunningRight or self.isRunningLeft:
            self.animation_timer += clock.get_time()
            if self.animation_timer >= self.animation_duration:
                self.running_animation_index = (self.running_animation_index + 1) % len(self.running_animation_frames)
                self.animation_timer = 0

        # Handle attack animation
        if self.is_attacking:
            self.animation_timer += clock.get_time()
            if self.animation_timer >= self.attack_animation_duration:
                self.attacking_animation_index = (self.attacking_animation_index + 1) % len(self.attacking_animation_frames)
                self.animation_timer = 0
                # Reset attack animation and cooldown when animation ends
                if self.attacking_animation_index == 0:
                    self.is_attacking = False
                    self.isIdle = True
                    self.attack_cooldown = self.attack_delay

        # Update position based on velocity
        self.x += self.xVel

        # Draw the appropriate animation frame based on player's state
        current_frame = None
        if self.isIdle:
            current_frame = self.idle_animation_frames[self.idle_animation_index]
        elif self.isRunningRight:
            current_frame = pygame.transform.flip(self.running_animation_frames[self.running_animation_index], True, False)
        elif self.isRunningLeft:
            current_frame = self.running_animation_frames[self.running_animation_index]
        elif self.is_attacking:
            current_frame = self.attacking_animation_frames[self.attacking_animation_index]

        if current_frame is not None:
            screen.blit(current_frame, (self.x - 50, self.y - 48))
                
               
    def draw_health_bar(self, surface):
         # Draw the outline of the health bar with a slight gradient effect
        pygame.draw.rect(surface, (100, 100, 100), (self.x - 25, self.y - 45, 102, 12))
        pygame.draw.rect(surface, (50, 50, 50), (self.x - 25, self.y - 45, 100, 10))

        # Calculate the width of the health bar based on the player's health
        health_width = int((self.health / 100) * 100)

        # Draw the health bar with a gradient effect
        health_color = (min(255, 255 - (self.health * 2.5)), max(0, self.health * 2.5), 0)
        pygame.draw.rect(surface, health_color, (self.x - 25, self.y - 45, health_width, 10))


def main_menu():
    pygame.display.update()
    player1.health = 100
    player2.health = 100
    player1.x = 100
    player2.x = 1325
    global currentState  # Declare currentState as a global variable
    if currentState == state[0]:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(main_menu_image, (0, 0))
        play_button = pygame.draw.rect(button_surface, (250, 0, 0), (620, 455, 200, 75))
        about_button = pygame.draw.rect(button_surface, (250, 0, 0), (620, 545, 200, 75))
        quit_button = pygame.draw.rect(button_surface, (250, 0, 0), (620, 645, 200, 75))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('mouse clicked')
                if play_button.collidepoint(mouse_pos):
                    print('start button pressed')
                    currentState = state[1]
                elif about_button.collidepoint(mouse_pos):
                    print('about button pressed')
                    currentState = state[2]
                elif quit_button.collidepoint(mouse_pos):
                    currentState = state[3]

            if event.type == pygame.QUIT:
                sys.exit()
                            

def about():
    global currentState
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(about_image, (0, 0))
    back_button = pygame.draw.rect(button_surface, (250, 0, 0), (580, 645, 240, 100))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse clicked')
            if back_button.collidepoint(mouse_pos):
                currentState = state[0]
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()

def exit():
    sys.exit(2)

player1 = Player(100, 650)
player2 = Player2(1325, 650)

def start():
    global currentState
    pygame.display.update()
    clock.tick(200)
    screen.fill((0, 0, 0))  # Fill the screen with black color
    check_collision(player1, player2)
    screen.blit(scaled_background, (0, 0))
    screen.blit(ground, (0, 750))
    events = pygame.event.get()  # Move this line inside the loop to update events continuously
    screen.blit(text_render, (screen_width // 5.5 - text_render.get_width() // 2, screen_height // 50 - text_render.get_height() // 2))
    screen.blit(text1_render, (screen_width // 5.5 - text_render.get_width() // 2, screen_height // 34 - text_render.get_height() // 900))
    player1.update(events)
    player2.update(events)

    if player2.health <= 0:
        print("Player 1 wins")
        currentState = state[4]
    if player1.health <= 0:
        currentState = state[5]

    pygame.display.update()



def check_collision(player1, player2):
    if player1.is_attacking and player2.x < player1.x + 150 and player2.x + 50 > player1.x + 50 and player1.y < player2.y + 100 and player1.y + 100 > player2.y:
        player2.health -= 3  # Deduct health if there's a collision
    # Check for collision between player 2's attack box and player 1's hit box
    if player2.is_attacking and player1.x < player2.x + 100 and player1.x + 50 > player2.x - 100 and player1.y < player2.y + 100 and player1.y + 100 > player2.y:
        player1.health -= 3



def player1_win():
    global currentState
    screen.blit(player1_win_screen, (0, 0))
    pygame.display.update()
    time.sleep(4)
    
    currentState = state[0]
    

def player2_win():
    global currentState
    screen.blit(player2_win_screen, (0,0))
    pygame.display.update()
    time.sleep(4)
    currentState = state[0]
   

# Game Loop
while True:
    print(currentState)
    if(currentState == state[1]):
        start()
    if(currentState == state[0]):
        main_menu()
    if(currentState == state[2]):
        about()
    if(currentState == state[3]):
        exit()
    if(currentState == state[4]):
        player1_win()
    if(currentState == state[5]):
        player2_win()
