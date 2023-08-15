# import libraries
import pygame
from pygame.locals import *
import math
import random

# import modules
from Castle import castle
from Enemies import enemies
from game_variabels import *
from help_function import *
from Castle import button

# initialise pygame
pygame.init()


def load_image(path):
    """
    help function for loading images
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert_alpha()


def draw_text(surface, text, font, text_color, x, y):
    """
    help function for drawing text
    :param surface: pygame.surface.Surface
    :param text: str
    :param font: pygame.font.Font
    :param text_color: tuple
    :param x: int     :param y: int
    """
    img = font.render(text, True, text_color)
    surface.blit(img, (x, y))


class Game:
    __instance = None

    @staticmethod
    def get_instance():
        if Game.__instance is None:
            Game.__instance = Game()
        return Game.__instance

    def __init__(self):
        super().__init__()
        if Game.__instance is None:
            Game.__instance = self

        global enemy_group

        # stages of the program
        self.game_over = False
        self.opening_game = True
        self.running = True

        # load castle images and create Castle
        self.castle = castle.Castle(screen_width - 250, screen_height - 350)

        # create button
        self.repair_button = button.Repair('repair', screen_width - 170, screen_height - 590,  upgrade_button_type_to_cost[repair_button])
        self.upgrade_health_button = button.Up_max_health('upgrade_health', screen_width - 90, screen_height - 590, upgrade_button_type_to_cost[upgrade_health_button])
        self.speed_button = button.Shooting_speed('speed', screen_width - 170, screen_height - 500, upgrade_button_type_to_cost[speed_button])
        self.attack_button = button.Attack('animation_type_attack', screen_width - 85, screen_height - 500,  upgrade_button_type_to_cost[attack_button])
        self.tower_button = button.Add_tower('tower', screen_width - 85, screen_height - 410,  upgrade_button_type_to_cost[tower_button])
        self.play_agine_button = button.Play_agine('play_agine', screen_width - 443, screen_height - 400, 0)
        self.start_game_button = button.Opening_game('start_game', screen_width/2, screen_height/2, 0)
        # buttons list
        self.upgrade_button_list = [self.repair_button, self.upgrade_health_button, self.speed_button, self.attack_button,
                            self.tower_button]
        self.game_button_list = [self.play_agine_button, self.start_game_button]

        self.upgrade_button_name_to_button = {repair_button: self.repair_button,
                                              upgrade_health_button: self.upgrade_health_button,
                                              speed_button: self.speed_button,
                                              attack_button: self.attack_button,
                                              tower_button: self.tower_button
                                              }

        self.game_button_name_to_button = {play_agine_button: self.play_agine_button,
                                           start_game_button: self.start_game_button}

        # create crosshair
        self.crosshair = castle.Crosshair(crosshair_scale_image)

        # enemies animation
        self.enemies_animation_list()

        # creat enemy_group
        enemy_group = pygame.sprite.Group()

    def run(self):
        """Game loop"""
        global LAST_ENEMY_ENTER, next_level, leve_difficulty, level, target_difficulty, level_reset_time, \
            next_level_font_30, next_level_font_60, WITH

        clock = pygame.time.Clock()
        FPS = 60

        while self.running:

            self.loop_event()

            if self.opening_game:
                self.draw_open_bg()
            elif not self.game_over:
                # draw the Game
                self.draw_game()
                if self.need_to_create_enemies():
                    self.create_enemies()
                elif self.is_end_level():
                    self.next_level()
                if self.level_reset_time_don():
                    self.move_to_next_level()
                if self.castle.health == 0:
                    self.game_over = True
            else:
                self.end_game()
            pygame.display.update()
            clock.tick(FPS)

    def end_game(self):
        pygame.mouse.set_visible(True)
        draw_text(surface, 'GAME OVER!', next_level_font_60, red_blood, 254, 100)
        draw_text(surface, 'Your Score: ' + str(self.castle.score), next_level_font_30, red_blood, 323, 150)
        draw_text(surface, 'Play agine! ', next_level_font_30, red_blood, 340, 180)
        self.play_agine_button.draw(surface)
        self.play_agine_button.press()

    def show_info(self):
        draw_text(surface, 'Level: ' + str(level), next_level_font_30, grey, screen_width - 790, screen_height - 590)
        draw_text(surface, 'Score: ' + str(self.castle.score), next_level_font_30, grey, screen_width - 530, screen_height - 590)
        draw_text(surface, 'High Score: ' + str(high_score), next_level_font_30, grey, screen_width - 530, screen_height - 555)
        draw_text(surface, 'Money: ' + str(self.castle.money), next_level_font_30, grey, screen_width - 790, screen_height - 555)
        draw_text(surface, 'Health: ' + str(self.castle.health) + "/" + str(self.castle.max_health),
                  next_level_font_30, grey, self.castle.rect.bottom, self.castle.rect.bottom + 10)
        draw_text(surface, 'Shooting speed: ' + str(self.castle.fire_speed), next_level_font_30, grey,
                  self.castle.rect.bottom, self.castle.rect.bottom + 43)
        draw_text(surface, 'Attack: ' + str(self.castle.attack), next_level_font_30, grey,
                  self.castle.rect.bottom, self.castle.rect.bottom + 75)
        for b in self.upgrade_button_list:
            if b == self.tower_button:
                if self.castle.num_towers < self.castle.max_num_tower:
                    draw_text(surface, str(b.coset), next_level_font_10, grey,b.rect.x, b.rect.y + 42)
                else:
                    draw_text(surface, 'max', next_level_font_10, grey, b.rect.x, b.rect.y + 42)
            elif b == self.speed_button:
                if self.castle.fire_speed <= self.castle.max_fire_speed:
                    draw_text(surface, str(b.coset), next_level_font_10, grey, b.rect.x + 10, b.rect.y + 50)
                else:
                    draw_text(surface, 'max', next_level_font_10, grey, b.rect.x + 10, b.rect.y + 50)
            else:
                draw_text(surface, str(b.coset), next_level_font_10, grey,
                          b.rect.x + 10, b.rect.y + 50)

    def draw_game(self):
        # draw background
        self.draw_bg()
        # draw castle
        self.castle.draw_castle()
        # draw towers
        self.castle.tower_group.draw(surface)
        # draw bullet of tower
        self.castle.tower_group.update(enemy_group)
        # draw crosshair
        self.crosshair.draw()
        # draw and activate buttons
        for b in self.upgrade_button_name_to_button:
            self.upgrade_button_name_to_button[b].draw(surface)
            self.upgrade_button_name_to_button[b].upgrade()
        # draw bullet of castle
        self.castle.fire()
        self.castle.bullet_group.update()
        self.castle.draw_bullets()
        # draw enemies
        enemy_group.update(surface, self.castle)
        # draw details
        self.show_info()

    def create_enemies(self):
        global LAST_ENEMY_ENTER, leve_difficulty
        # create enemies and them to the group
        if pygame.time.get_ticks() - LAST_ENEMY_ENTER > ENEMY_ENTER:
            for enemy_type in enemies_type:
                if random.randint(0, 99) / 100 < 0.4:
                    enemy = enemies.Enemies(enemies_animation[0], knight, -100, screen_height - 100, level)
                elif random.randint(0, 99) / 100 < 0.4:
                    enemy = enemies.Enemies(enemies_animation[1], goblin, -100, screen_height - 100, level)
                elif random.randint(0, 99) / 100 < 0.4:
                    enemy = enemies.Enemies(enemies_animation[2], purple_goblin, -100, screen_height - 100
                                            , level)
                else:
                    enemy = enemies.Enemies(enemies_animation[3], red_goblin, -100, screen_height - 100
                                            , level)
            enemy_group.add(enemy)
            # update LAST_ENEMY_ENTER
            LAST_ENEMY_ENTER = pygame.time.get_ticks()
            # increase level difficulty by enemy health
            leve_difficulty += enemies_health[0]

    def enemies_animation_list(self):
        global enemies_type, enemies_animation, enemies_health, enemies_alive
        for enemy in enemies_type:
            # load animation
            animation_list = []
            for animation in animation_type:
                # reset temporary list of images
                temp_list = []
                # define number of frame
                num_of_frame = 20
                for i in range(num_of_frame):
                    e_img = load_image(f"img/enemies/{enemy}/{animation}/{i}.png")
                    e_w = e_img.get_width()
                    e_h = e_img.get_height()
                    e_img = pygame.transform.scale(e_img, (int(e_w) * enemies_scale_image, (int(e_h) * enemies_scale_image)))
                    temp_list.append(e_img)
                animation_list.append(temp_list)
            enemies_animation.append(animation_list)

    def next_level(self):
        global next_level, enemies_alive, level_reset_time
        # check how many is still alive
        enemies_alive = 0
        for e in enemy_group:
            if e.alive:
                enemies_alive += 1
        # if there are none enemies alive the level is complete
        if enemies_alive == 0 and not next_level:
            next_level = True
            level_reset_time = pygame.time.get_ticks()
        if next_level:
            draw_text(surface, 'MOVING TO THE NEXT LEVEL!', next_level_font_30, red_blood, screen_width/2 - 200, screen_height/2 -100)

    def move_to_next_level(self):
        global next_level, level, LAST_ENEMY_ENTER, target_difficulty, leve_difficulty

        next_level = False
        level += 1
        LAST_ENEMY_ENTER = pygame.time.get_ticks()
        target_difficulty *= DIFFICULTY_MULTIPLIER
        leve_difficulty = 0
        enemy_group.empty()

    def loop_event(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == QUIT:
                self.running = False
        return self.running

    def reset(self):
        global level, leve_difficulty, target_difficulty, next_level, DIFFICULTY_MULTIPLIER, enemies_alive, ENEMY_ENTER \
            , LAST_ENEMY_ENTER, level_reset_time
        self.castle.reset()
        self.running = True
        self.game_over = False
        enemy_group.empty()
        pygame.mouse.set_visible(False)
        for (b, c) in zip(self.upgrade_button_list, upgrade_button_type_to_cost):
            b.set_cost(upgrade_button_type_to_cost[c])

        level = 1
        leve_difficulty = 0
        target_difficulty = 1000
        next_level = False
        DIFFICULTY_MULTIPLIER = 1.1

        enemies_alive = 0
        ENEMY_ENTER = 1000
        LAST_ENEMY_ENTER = pygame.time.get_ticks()
        level_reset_time = pygame.time.get_ticks()

    def update_high_score(self):
        global high_score
        if self.castle.score > high_score:
            high_score = self.castle.score
            with open('score.txt', 'w') as f:
                f.write(str(high_score))

    def draw_bg(self):
        surface.blit(bg, (0, 0))

    def draw_open_bg(self):
        pygame.mouse.set_visible(True)
        self.draw_bg()
        draw_text(surface, 'Lets Start The GAME!!', next_level_font_60, red_blood, screen_width/2 - screen_width/4, screen_height/2 - 70)
        self.game_button_name_to_button[start_game_button].draw(surface)
        self.game_button_name_to_button[start_game_button].press()
        self.game_button_name_to_button[play_agine_button].press()

    def need_to_create_enemies(self):
        return leve_difficulty < target_difficulty

    def is_end_level(self):
        return leve_difficulty >= target_difficulty

    def level_reset_time_don(self):
        return pygame.time.get_ticks() - level_reset_time > 1500 and next_level
