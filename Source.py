import pygame
import os
import time
import random

# Initializing pygame and font
pygame.font.init()
pygame.init()

# Configuration Dictionary
config = {'screen_width': 700, 'screen_height': 450, 'FPS': 60, 'initial_lives': 3, 'shoot_cooldown': 200, 'player_vel': 5, 'laser_vel': 5, 'boost_vel': 3, 'enemy_vel': 0.5, 'wave_length': 3}

# Initializing screen
screen = pygame.display.set_mode((700, 450))

# Loading players, enemy, boost, and power_up
space_ship = pygame.image.load(os.path.join('Enemy.png'))
Y_ship = pygame.image.load(os.path.join('Player.png'))
Laser = pygame.image.load(os.path.join("Laser.png"))
Boost = pygame.image.load(os.path.join("Boost1.png"))
Boost1 = pygame.image.load(os.path.join("Boost2.png"))
BG = pygame.image.load(os.path.join("BCKGROUND.png"))

# Defining class for Ship, Enemy, and Power_ups
class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))

class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        scaled_image = pygame.transform.scale(Y_ship, (Y_ship.get_width() // 2, Y_ship.get_height() // 2))
        self.ship_img = scaled_image
        self.laser_img = Laser
        self.mask = pygame.mask.from_surface(self.ship_img)

class Enemy(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        scaled_image = pygame.transform.scale(space_ship, (space_ship.get_width() // 2, space_ship.get_height() // 2))
        self.ship_img = scaled_image
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.boost_img = pygame.transform.scale(Boost, (Boost.get_width()//1.30 ,Boost.get_height()//1.30))

    def move(self, vel):
        self.y += vel

    def draw(self, screen):
        screen.blit(self.boost_img, (self.x, self.y))

class PowerUp1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.boost_img = pygame.transform.scale(Boost1, (Boost1.get_width()//6 ,Boost1.get_height()//6))

    def move(self, vel):
        self.y += vel

    def draw(self, screen):
        screen.blit(self.boost_img, (self.x, self.y))

# Generating stack of enemies through recursion
def generate_wave(wave_length, enemies):
    if len(enemies) == wave_length:
        return
    else:
        enemy = Enemy(random.randrange(10, 650), -random.randrange(1, 600))
        enemies.append(enemy)
        generate_wave(wave_length, enemies)

# Main game loop
def main_loop():
    # Declaring initial values to game attributes
    FPS = config['FPS'] #using dictionary keys to access values
    level = 0
    score = 0
    lives = config['initial_lives']
    player_lasers = []
    last_shot_time = 0
    shoot_cooldown = config['shoot_cooldown']
    player_vel = config['player_vel']
    laser_vel = config['laser_vel']
    current_time = 0
    main_font = pygame.font.SysFont('comicsans', 25)
    lost_font = pygame.font.SysFont('comicsans', 70)
    # saving enemies, power_ups and vel_powerups as nested list
    enemies = []
    power_ups = []
    vel_powerups = [] 
    wave_length = config['wave_length']
    enemy_vel = config['enemy_vel']
    boost_vel = config['boost_vel']
    boost_counter = 0
    vel_boost_counter = 0
    player = Player(350, 380)
    clock = pygame.time.Clock()

    # Making functions to draw and move game characters
    def move_lasers(lasers, vel):
        for laser in lasers:
            laser[1] -= vel

    def draw_lasers(lasers):
        for laser in lasers:
            screen.blit(Laser, (laser[0], laser[1]))

    def move_power_ups(power_ups, vel):
        for power_up in power_ups:
            power_up.move(vel)

    def draw_power_ups(power_ups):
        for power_up in power_ups:
            power_up.draw(screen)
    
    def move_power_ups1(vel_powerups, vel):
        for power_up in vel_powerups:
            power_up.move(vel)

    def draw_power_ups1(vel_powerups):
        for power_up in vel_powerups:
            power_up.draw(screen)

    # Generating enemies through recursion
    def generate_next_wave():
        nonlocal level, wave_length, enemy_vel, enemies, lives
        wave_length += 1
        enemy_vel += 0.35
        if lives > 0:
            level += 1
            generate_wave(wave_length, enemies)

            # Add a Boost power-up after every two levels
            if level % 2 == 0:
                power_up = PowerUp(random.randint(10, 650), -random.randint(1, 100))
                power_ups.append(power_up)
            if level%3 == 0:
                power_up1 = PowerUp1(random.randint(10, 650), -random.randint(1, 100))
                vel_powerups.append(power_up1)

    # Check enemy collision
    def check_collision_enemy(enemies, lasers, score):
        for enemy in list(enemies):
            for laser in lasers[:]:
                # Use Rect.colliderect method for collision detection
                if pygame.Rect(enemy.x, enemy.y, enemy.ship_img.get_width(), enemy.ship_img.get_height()).colliderect(
                        pygame.Rect(laser[0], laser[1], Laser.get_width(), Laser.get_height())
                ):
                    enemies.remove(enemy)
                    lasers.remove(laser)
                    score += 1  # Update the outer score variable
                    return True
        return False
    #check for power_up Collision
    def check_collision_power_up(power_ups):
        for power_up in power_ups[:]:
            if pygame.Rect(player.x, player.y, player.ship_img.get_width(), player.ship_img.get_height()).colliderect(
                    pygame.Rect(power_up.x, power_up.y, Boost.get_width(), Boost.get_height())
            ):
                power_ups.remove(power_up)
                return True

        return False
    #check for power_up1 Collision
    def check_collision_power_up1(vel_powerups):
        for power_up in vel_powerups[:]:
            if pygame.Rect(player.x, player.y, player.ship_img.get_width(), player.ship_img.get_height()).colliderect(
                    pygame.Rect(power_up.x, power_up.y, Boost1.get_width(), Boost1.get_height())
            ):
                vel_powerups.remove(power_up)
                return True

        return False


    def redraw_window():
        screen.blit(BG, (0, 0))
        #initializing Stats
        lives_remaining = main_font.render(f"Lives: {lives}", 1, (0, 255, 0))
        Power_ups_gained = main_font.render(f"Boosts: {boost_counter}", 1, (0, 255, 0))
        Power_up1_gained = main_font.render(f"Decelerator: {vel_boost_counter}", 1, (0, 255, 0))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        # displaying stats on screen
        screen.blit(lives_remaining, (10, 10))
        screen.blit(level_label, (700 - level_label.get_width() - 10, 10))
        screen.blit(Power_up1_gained,(10, Power_ups_gained.get_height() + 40))
        screen.blit(score_label, (700 - level_label.get_width() - 30, level_label.get_height() + 10))
        screen.blit(Power_ups_gained, (10, lives_remaining.get_height() + 10))

        # Drawing power-ups on screen from list
        for power_up in power_ups:
            power_up.draw(screen)
        for j in vel_powerups:
            j.draw(screen)
        # If the player still has lives, then generate more enemies
        if lives <= 0:
            lost_label = lost_font.render("You Lost", 1, (255, 255, 255))
            screen.blit(lost_label, (350 - lost_label.get_width() / 2, 200))
        else:
            for enemy in enemies:
                enemy.draw(screen)
            player.draw(screen)
            draw_lasers(player_lasers)
        pygame.display.update()

    # Running condition as True for the main loop
    run = True
    while run:
        #integrating Time with Clock
        clock.tick(FPS)

        # Generating next wave
        if len(enemies) == 0:
            generate_next_wave()

        # Updating current Time
        current_time = pygame.time.get_ticks()

        # Event Handler main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Checking for keys getting pressed on the keyboard and their respective tasks
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel < 650:
            player.x += player_vel

        if keys[pygame.K_w] and (current_time - last_shot_time) >= shoot_cooldown:
            laser_x = player.x + (player.ship_img.get_width() // 2) - (Laser.get_width() // 2)
            laser_y = player.y - Laser.get_height()
            player_lasers.append([laser_x, laser_y])
            last_shot_time = current_time

        if keys[pygame.K_SPACE] and boost_counter > 0:
            enemies.clear()
            boost_counter -= 1

        if keys[pygame.K_r] and vel_boost_counter > 0:
            if enemy_vel>0.75:
                enemy_vel -= 0.75
            vel_boost_counter -= 1

        # Moving enemies and checking for their collision with the ground
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.ship_img.get_height() > 450:
                enemies.remove(enemy)
                lives -= 1

        # Call to check for enemy collision
        if check_collision_enemy(enemies, player_lasers, score):
            score += 1
        
        #check for powr_up collision
        if check_collision_power_up(power_ups):
            boost_counter += 1
        if check_collision_power_up1(vel_powerups):
            vel_boost_counter += 1
        # Call to move lasers and power-ups
        move_lasers(player_lasers, laser_vel)
        draw_power_ups(power_ups)
        move_power_ups(power_ups, boost_vel)
        draw_power_ups1(vel_powerups)
        move_power_ups1(vel_powerups, boost_vel)

        # Updating pygame window
        redraw_window()

    # Closing pygame
    pygame.quit()

main_loop()
