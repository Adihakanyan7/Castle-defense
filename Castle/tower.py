# import library
import pygame
import math

# import modules
from Game import game
from Castle import weapon
from game_variabels import *


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game.Game.get_instance()
        self.get_target = False
        self.health = self.game.castle.health
        self.max_health = self.game.castle.max_health
        self.fire_speed = tower_fire_speed
        self.attack = tower_attack
        self.e_target_x, self.e_target_y = 0, 0
        self.lest_shoot = pygame.time.get_ticks()

        # create the rectangle of the image
        self.image = tower_image_100_percent_health_image
        self.rect = tower_image_100_percent_health_image.get_rect()
        self.set_rect_x_y(x, y)

        self.angle = self.create_angle(0, 0)  # need the rectangle of the tower

        # create a group
        self.bullet_group = pygame.sprite.Group()

        # create bullet
        self.bullet = weapon.Bullet_tower(self.rect.midleft[0], self.rect.midleft[1], self.angle,
                                          self.fire_speed, self.attack)

    def update(self, enemy_group):
        # tower image
        if self.game.castle.health / self.max_health <= 0.25:
            self.image = tower_image_25_percent_health_image
        elif self.game.castle.health / self.max_health <= 0.50:
            self.image = tower_image_50_percent_health_image
        else:
            self.image = tower_image_100_percent_health_image
        surface.blit(self.image, self.rect)

        # get a target
        self.get_target = False
        for e in enemy_group:
            if e.alive:
                e_target_x, e_target_y = e.rect.center
                self.get_target = True
                break

        # shoot
        if self.get_target:
            self.angle = self.create_angle(e_target_x, e_target_y)
            # add the bullet to the bullet_group
            if pygame.time.get_ticks() - self.lest_shoot > tower_shot_cooldown:
                self.lest_shoot = pygame.time.get_ticks()
                self.bullet = weapon.Bullet_tower(self.rect.midleft[0], self.rect.midleft[1], self.angle,
                                                  self.fire_speed, self.attack)
                self.bullet_group.add(self.bullet)

        self.bullet_group.update()
        self.bullet_group.draw(surface)

    # help function for the constructor
    def set_rect_x_y(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def create_angle(self, t_x, t_y):
        x_dist = t_x - self.rect.midleft[0]
        y_dist = -(t_y - self.rect.midleft[1])
        return math.degrees(math.atan2(y_dist, x_dist))
