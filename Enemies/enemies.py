from game_variabels import *
from Game import game


class Enemies(pygame.sprite.Sprite):
    def __init__(self, animation_list, enemy_type, x, y, level_game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game.Game.get_instance()
        self.alive = True
        self.type = enemy_type
        self.health = enemies_characteristics[self.type][enemy_health] + int(1.1 * level_game)
        self.power = enemies_characteristics[self.type][enemy_power] + int(1.1 * level_game)
        self.speed = enemies_characteristics[self.type][enemy_speed] + int(1.1 * level_game)
        self.money = enemies_characteristics[self.type][enemy_money] + int(1.1 * level_game)
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000
        self.animation_list = animation_list
        self.action = 0  # 0:animation_type_walk, 1:animation_type_attack, 2:animation_type_death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # select starting image
        self.img = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 30, 45)
        self.rect.center = (x, y - 80)

    def update(self, surface, castle):
        if self.alive:
            # checking if the enemy collided with the bullet
            if pygame.sprite.spritecollide(self, castle.bullet_group, True):
                self.health -= self.game.castle.bullet.attack
            for tower in castle.tower_list:
                if pygame.sprite.spritecollide(self, tower.bullet_group, True):
                    self.health -= tower.bullet.attack

            # check if the enemy reached the castle
            if self.rect.right > castle.rect.left:
                self.update_action(1)

            if self.health <= 0:
                self.alive = False
                castle.money += self.money
                castle.score += self.money
                self.update_action(2)

            # move enemy
            if self.action == 0:
                # update rectangle position
                self.rect.x += self.speed

            # animation_type_attack
            if self.action == 1:
                # check if enough time is fast since the last animation_type_attack
                if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                    # dile damage to the castle
                    castle.health -= self.power
                    if castle.health <= 0:
                        castle.health = 0
                    self.last_attack = pygame.time.get_ticks()



        self.update_animation()

        # draw image on screen
        surface.blit(self.img, (self.rect.x - 10, self.rect.y - 15))

    def update_animation(self):
        # update image according to current action
        self.img = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > enemy_animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])

    def update_action(self, action):
        if self.action != action:
            self.action = action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
