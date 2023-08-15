# import librairy
import pygame
import math
from abc import ABC, abstractmethod

# import modules
from game_variabels import *


def load_image(path):
    """
    help function for loading images
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert_alpha()


class Weapon(ABC):
    def __init__(self, x, y, angle, speed, attack):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle_degrees = angle
        self.angle_radians = math.radians(angle)  # convert angle to radians
        self.speed = speed
        self.attack = attack
        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(self.angle_radians) * self.speed
        self.dy = -(math.sin(self.angle_radians) * self.speed)

    @abstractmethod
    def update(self):
        pass


class Bullet_castle(Weapon, pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, attack):
        pygame.sprite.Sprite.__init__(self)
        self.image = castle_weapon_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle_degrees = angle
        self.angle_radians = math.radians(angle)  # convert angle to radians
        self.speed = speed
        self.attack = attack
        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(self.angle_radians) * self.speed
        self.dy = -(math.sin(self.angle_radians) * self.speed)

    def update(self):
        """move the bullet and remove if the bullet goes out of the screen"""
        # check if the bullet is goes out of the screen
        if ((self.rect.right < 0) or (self.rect.left > screen_width) or (self.rect.top < 0) or
            (self.rect.bottom > screen_height - 75)) or (-60 < self.angle_degrees < 130):
            self.kill()

        # move
        self.rect.x += self.dx
        self.rect.y += self.dy


class Bullet_tower(Weapon, pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, attack):
        pygame.sprite.Sprite.__init__(self)
        self.image = tower_weapon_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle_degrees = angle
        self.angle_radians = math.radians(angle)  # convert angle to radians
        self.speed = speed
        self.attack = attack
        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(self.angle_radians) * self.speed
        self.dy = -(math.sin(self.angle_radians) * self.speed)

    def update(self):
        """move the bullet and remove if the bullet goes out of the screen"""
        # check if the bullet is goes out of the screen
        if ((self.rect.right < 0) or (self.rect.left > screen_width) or (self.rect.top < 0) or
                (self.rect.bottom > screen_width - 75)):
            self.kill()

        # move
        self.rect.x += self.dx
        self.rect.y += self.dy
