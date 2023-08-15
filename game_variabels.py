# import library
import pygame
import os

# import modules
# from help_function import *

# initialise pygame
pygame.init()


def load_image(path):
    """
    help function for loading images
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert_alpha()


def load_transfer_image(phat, scale):
    castle = load_image(phat)  # Castle 25% health

    width = castle.get_width()
    height = castle.get_height()

    return pygame.transform.scale(castle, (int(width * scale), int(height * scale)))


# define Game variables

# Game window
screen_width = 800
screen_height = 600

# fonts
next_level_font_10 = pygame.font.SysFont('Futura', 26)
next_level_font_30 = pygame.font.SysFont('Futura', 30)
next_level_font_60 = pygame.font.SysFont('Futura', 60)

# colors
whit = (255, 255, 255)
red_blood = (115, 23, 16)
grey = (100, 100, 100)

# start_game
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Castle Defender")

# Scale images

# castle
castle_scale_image = 0.2
castle_bullet_scale_image = 0.09

# crosshair
crosshair_scale_image = 0.025

# towers
tower_scale_image = 0.2
tower_bullet_scale_image = 0.09

# enemies
enemies_scale_image = 0.3

# buttons
repair_button_scale_image = 0.5
max_health_button_scale_image = 1.2
speed_button_scale_image = 0.35
attack_button_scale_image = 0.7
tower_button_scale_image = 0.7
play_agine_button_scale_image = 2
start_game_button_scale_image = 2

# Images

# background
bg = load_image('img/bg.png')

# castle
castle_25_percent_health_image = load_transfer_image('img/Castle/castle_25.png', castle_scale_image)
castle_50_percent_health_image = load_transfer_image('img/Castle/castle_50.png', castle_scale_image)
castle_100_percent_health_image = load_transfer_image('img/Castle/castle_100.png', castle_scale_image)
castle_weapon_image = load_transfer_image('img/bullet.png', castle_bullet_scale_image)

# towers
tower_image_25_percent_health_image = load_transfer_image('img/tower/tower_25.png',
                                                          tower_scale_image)  # castle 25% health
tower_image_50_percent_health_image = load_transfer_image('img/tower/tower_50.png', tower_scale_image)
tower_image_100_percent_health_image = load_transfer_image('img/tower/tower_100.png', tower_scale_image)
tower_weapon_image = load_transfer_image('img/bullet.png', tower_bullet_scale_image)

# buttons
button_repair_image = load_transfer_image('img/repair.png', repair_button_scale_image)  # castle 25% health
button_upgrade_health_image = load_transfer_image('img/armour.png', max_health_button_scale_image)
button_speed_image = load_transfer_image('img/gunsight.png', speed_button_scale_image)
button_attack_image = load_transfer_image('img/ammunition.png', attack_button_scale_image)
button_tower_image = load_transfer_image('img/tower.png', tower_button_scale_image)
button_start_game_image = load_transfer_image('img/play.png', play_agine_button_scale_image)
button_play_agine_image = load_transfer_image('img/play.png', start_game_button_scale_image)

# Buttons

# names of the buttons
repair_button = 'repair'
upgrade_health_button = 'upgrade_health'
speed_button = 'speed'
attack_button = 'animation_type_attack'
tower_button = 'tower'
play_agine_button = 'play_agine'
start_game_button = 'start_game'

upgrade_button_to_image = {repair_button: button_repair_image,
                           upgrade_health_button: button_upgrade_health_image,
                           speed_button: button_speed_image,
                           attack_button: button_attack_image,
                           tower_button: button_tower_image
                           }

game_button_to_image = {'play_agine': button_start_game_image,
                        'start_game': button_play_agine_image}

upgrade_button_type_to_cost = {repair_button: 300,
                               upgrade_health_button: 300,
                               speed_button: 500,
                               attack_button: 200,
                               tower_button: 2000,
                               }

# levels
high_score = 0
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
level = 1
leve_difficulty = 0
target_difficulty = 1000
next_level = False
DIFFICULTY_MULTIPLIER = 1.1

# enemies
enemies_alive = 0
ENEMY_ENTER = 1000
LAST_ENEMY_ENTER = pygame.time.get_ticks()
level_reset_time = pygame.time.get_ticks()

# define animation cooldown
enemy_animation_cooldown = 50

enemies_animation = []
# enemies names
knight = 'knight'
goblin = 'goblin'
purple_goblin = 'purple_goblin'
red_goblin = 'red_goblin'

# animation_type_names
animation_type_walk = 'animation_type_walk'
animation_type_attack = 'animation_type_attack'
animation_type_death = 'animation_type_death'


# enemies characteristics names
enemy_health = 'enemy_health'
enemy_power = 'enemy_power'
enemy_speed = 'enemy_speed'
enemy_money = 'enemy_money'
enemies_characteristics = {knight: {enemy_health: 75,
                                    enemy_power: 25,
                                    enemy_speed: 2,
                                    enemy_money: 50},
                           goblin: {enemy_health: 100,
                                    enemy_power: 50,
                                    enemy_speed: 1,
                                    enemy_money: 75},
                           purple_goblin: {enemy_health: 250,
                                           enemy_power: 15,
                                           enemy_speed: 1,
                                           enemy_money: 100},
                           red_goblin: {enemy_health: 250,
                                        enemy_power: 50,
                                        enemy_speed: 0.75,
                                        enemy_money: 150}}

enemies_health = [75, 100, 125, 150]
enemies_type = [knight, goblin, purple_goblin, red_goblin]
animation_type = [animation_type_walk, animation_type_attack, animation_type_death]

# castle
castle_money = 500
castle_score = 0
castle_fire_speed = 3
max_castle_fire_speed = 35
castle_health = 1000
castle_attack = 25
castle_max_health = castle_health
castle_tower_list = []
castle_num_towers = 0
castle_max_num_tower = 2

# towers
tower_fire_speed = 5
tower_attack = 100
tower_shot_cooldown = 1000
towers = {"0": (screen_width - 450, screen_height - 330),
          "1": (screen_width - 530, screen_height - 330)}
