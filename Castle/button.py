# import library's
from abc import ABC, abstractmethod

# import modules
from Game import game
from game_variabels import *

pygame.init()


class Button(ABC):
    def __init__(self, button_type, x, y, price):
        self.g = game.Game.get_instance()
        self.typ = button_type
        if button_type in upgrade_button_to_image:
            self.image = upgrade_button_to_image[button_type]
        else:
            self.image = game_button_to_image[button_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.action = False
        self.coset = price

    def draw(self, surface):
        global repair_image, armour_image, speed_image, attack_image
        # mouse position
        pos = pygame.mouse.get_pos()

        # check if mouse clicked the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def set_cost(self, cost):
        self.coset = cost

    @abstractmethod
    def upgrade(self):
        pass


class Shooting_speed(Button):

    def __init__(self, button_type, x, y, price):
        super().__init__(button_type, x, y, price)

    def upgrade(self):
        if self.action:
            if game.Game.get_instance().castle.money >= self.coset and game.Game.get_instance().castle.fire_speed <= max_castle_fire_speed:
                game.Game.get_instance().castle.money -= self.coset
                game.Game.get_instance().castle.fire_speed += 3
                self.coset += int((self.coset * 0.5) + (100 - ((self.coset * 0.5) % 100)))
        self.action = False


class Repair(Button):

    def __init__(self, button_type, x, y, price):
        super().__init__(button_type, x, y, price)

    def upgrade(self):
        if self.action:
            if (game.Game.get_instance().castle.money >= self.coset and
                    game.Game.get_instance().castle.health < game.Game.get_instance().castle.max_health):
                game.Game.get_instance().castle.money -= self.coset
                game.Game.get_instance().castle.health += 500
                if game.Game.get_instance().castle.health > game.Game.get_instance().castle.max_health:
                    game.Game.get_instance().castle.health = game.Game.get_instance().castle.max_health
                self.coset += 100
        self.action = False


class Up_max_health(Button):

    def __init__(self, button_type, x, y, price):
        super().__init__(button_type, x, y, price)

    def upgrade(self):
        if self.action:
            if game.Game.get_instance().castle.money >= self.coset:
                game.Game.get_instance().castle.money -= self.coset
                game.Game.get_instance().castle.health += 300
                game.Game.get_instance().castle.max_health += 300
                self.coset += int((self.coset * 0.5) + (100 - ((self.coset * 0.5) % 100)))
        self.action = False


class Attack(Button):

    def __init__(self, button_type, x, y, price):
        super().__init__(button_type, x, y, price)
        self.rect.topleft = (x - 5, y)

    def upgrade(self):
        if self.action:
            if game.Game.get_instance().castle.money >= self.coset:
                game.Game.get_instance().castle.money -= self.coset
                game.Game.get_instance().castle.attack += 10
                self.coset += int((self.coset * 0.3) + (100 - ((self.coset * 0.3) % 100)))
        self.action = False


class Add_tower(Button):

    def __init__(self, button_type, x, y, price):
        super().__init__(button_type, x, y, price)
        self.rect.topleft = (x - 2, y)

    def upgrade(self):
        if self.action and game.Game.get_instance().castle.num_towers < game.Game.get_instance().castle.max_num_tower:
            if game.Game.get_instance().castle.money >= self.coset:
                game.Game.get_instance().castle.money -= self.coset
                game.Game.get_instance().castle.create_tower(
                    towers[str(game.Game.get_instance().castle.num_towers)][0],
                    towers[str(game.Game.get_instance().castle.num_towers)][1])
                game.Game.get_instance().castle.num_towers += 1
                self.coset += int((self.coset * 0.3) + (100 - ((self.coset * 0.3) % 100)))
        self.action = False

class Play_agine(Button):

    def __init__(self, button_type, x, y, price):
        super().__init__(button_type, x, y, price)
        self.rect.topleft = (x - 2, y)

    def upgrade(self):
        pass

    def press(self):
        if self.action:
            self.g.update_high_score()
            self.g.reset()
        self.action = False


class Opening_game(Button):

    def __init__(self, button_type, x, y, price):
        super().__init__(button_type, x, y, price)
        self.rect.topleft = (x - 2, y)

    def upgrade(self):
        pass

    def press(self):
        if self.action:
            self.g.opening_game = False
        self.action = False
