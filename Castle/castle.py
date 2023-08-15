# import librairy
import math

# import module
from Castle import weapon, tower
from game_variabels import *

pygame.init()


class Castle:
    __instance = None

    @staticmethod
    def get_instance():
        if Castle.__instance is None:
            Castle.__instance = Castle(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 350)
        return Castle.__instance

    def __init__(self, x, y):
        super().__init__()
        if Castle.__instance is None:
            Castle.__instance = self

        # limit mouse click
        self.fire_bullet = False

        self.image = None
        self.money = castle_money
        self.score = castle_score
        self.fire_speed = castle_fire_speed
        self.max_fire_speed = max_castle_fire_speed
        self.health = castle_health
        self.attack = castle_attack
        self.max_health = castle_max_health
        self.tower_list = castle_tower_list
        self.num_towers = castle_num_towers
        self.max_num_tower = castle_max_num_tower

        # create the rectangle of the image
        self.rect = castle_100_percent_health_image.get_rect()
        self.set_rect_x_y(x, y)

        self.angle = self.create_angle()  # need the rect of the castle

        # create a group
        self.bullet_group = pygame.sprite.Group()
        self.tower_group = pygame.sprite.Group()

        # create bullet
        self.bullet = weapon.Bullet_castle(self.rect.midleft[0], self.rect.midleft[1], self.angle,
                                           self.fire_speed, self.attack)

    def reset(self):
        self.money = castle_money
        self.score = castle_score
        self.fire_speed = castle_fire_speed
        self.health = castle_health
        self.attack = castle_attack
        self.max_health = castle_max_health
        self.tower_list = castle_tower_list
        self.num_towers = castle_num_towers
        self.max_num_tower = castle_max_num_tower
        self.bullet_group.empty()
        self.tower_group.empty()
        self.bullet = weapon.Bullet_castle(self.rect.midleft[0], self.rect.midleft[1], self.angle,
                                           self.fire_speed, self.attack)

        self.fire_bullet = False

    def draw_castle(self):
        if self.health / self.max_health <= 0.25:
            self.image = castle_25_percent_health_image
        elif self.health / self.max_health <= 0.50:
            self.image = castle_50_percent_health_image
        else:
            self.image = castle_100_percent_health_image
        surface.blit(self.image, self.rect)

    def draw_bullets(self):
        self.bullet_group.draw(surface)

    def fire(self):
        self.angle = self.create_angle()

        # add the bullet to the bullet_group
        if pygame.mouse.get_pressed()[0] and not self.fire_bullet:
            self.fire_bullet = True
            self.bullet = weapon.Bullet_castle(self.rect.midleft[0], self.rect.midleft[1], self.angle,
                                               self.fire_speed, self.attack)
            self.bullet_group.add(self.bullet)
        # reset mouse click
        if not pygame.mouse.get_pressed()[0]:
            self.fire_bullet = False

    # help function for the constructor
    def set_rect_x_y(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def load_castle_image(self, path):
        castle_image = pygame.image.load(path).convert_alpha()

        return castle_image

    def load_transfer_image(self, phat, scale):
        castle = self.load_castle_image(phat)  # Castle 25% health

        width_25 = castle.get_width()
        height_25 = castle.get_height()

        return pygame.transform.scale(castle, (int(width_25 * scale), int(height_25 * scale)))

    def create_angle(self):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = -(pos[1] - self.rect.midleft[1])
        return math.degrees(math.atan2(y_dist, x_dist))

    def create_tower(self, x, y):
        if self.num_towers < self.max_num_tower:
            new_tower = tower.Tower(x, y)
            self.tower_list.append(new_tower)
            self.tower_group.add(new_tower)


class Crosshair():
    def __init__(self, scal):
        image = pygame.image.load("img/crosshair.png")
        c_w = image.get_width()
        c_h = image.get_height()

        self.image = pygame.transform.scale(image, (int(c_w * scal), int(c_h * scal)))
        self.rect = self.image.get_rect()

        # hide the mouse
        pygame.mouse.set_visible(False)

    def draw(self):
        # position of the mouse
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        surface.blit(self.image, self.rect)
