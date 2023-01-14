import pygame
import sys

from source.settings import PLAYER_SPRITE, WINDOW_SIZE
from source.animated_sprite import AnimatedSprite
from source.load_image import load_image
from source.bullet import Bullet


class Player(AnimatedSprite):
    image = load_image(PLAYER_SPRITE)
    MAX_SPEED = 10

    def __init__(self, sheet, columns, rows, x, y, acceleration, bullet_count, player_group, bullet_group):
        super().__init__(sheet, columns, rows, x, y, player_group)
        self.rect = self.image.get_rect()
        self.rect.bottom = WINDOW_SIZE[1] - 100
        self.rect.centerx = WINDOW_SIZE[0] // 2
        self.mask = pygame.mask.from_surface(self.image)

        self.bullet_group = bullet_group

        self.acceleration = acceleration
        self.bullet_count = bullet_count
        self.velocity = [0, 0]

        self.is_stopped = False

    def shoot(self):
        if self.bullet_count > 0 and not self.is_stopped:
            self.bullet_count -= 2
            Bullet(self.rect.x, self.rect.y, 19, 15, self.bullet_group)
            Bullet(self.rect.x, self.rect.y, 47, 15, self.bullet_group)

    def check_max_speed(self):
        if self.velocity[0] > Player.MAX_SPEED:
            self.velocity[0] = Player.MAX_SPEED
        elif self.velocity[0] < -Player.MAX_SPEED:
            self.velocity[0] = -Player.MAX_SPEED

    def accelerate_right(self):
        self.velocity[0] += self.acceleration[0]
        self.check_max_speed()

    def accelerate_left(self):
        self.velocity[0] -= self.acceleration[0]
        self.check_max_speed()

    def auto_acceleration_stop(self):
        # if self.velocity[0] > 0:
        #     if self.velocity[0] - math.sqrt(abs(self.velocity[0])) > 0:
        #         self.velocity[0] -= math.sqrt(abs(self.velocity[0]))
        #     else:
        #         self.velocity[0] -= self.velocity[0]
        #
        # elif self.velocity[0] < 0:
        #     if self.velocity[0] + math.sqrt(abs(self.velocity[0])) < 0:
        #         self.velocity[0] += math.sqrt(abs(self.velocity[0]))
        #     else:
        #         self.velocity[0] -= self.velocity[0]
        self.velocity[0] = 0

    def check_position(self):
        if self.rect.x > WINDOW_SIZE[0] - self.rect.width:
            self.rect.x = WINDOW_SIZE[0] - self.rect.width
            self.velocity[0] = 0
        elif self.rect.x < 0:
            self.rect.x = 0
            self.velocity[0] = 0

    def collision_check(self, enemy_group):
        for enemy in enemy_group:
            if pygame.sprite.collide_mask(self, enemy):
                enemy.kill()
                self.kill()

    def pick_up_bonus(self, bonus_group):
        for sprite in bonus_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.bullet_count += 20
                sprite.kill()

    def move(self):
        if not self.is_stopped:
            self.rect.right += self.velocity[0]
        self.check_position()
        # self.collision_check()
        # self.pick_up_bonus()

    def stop(self):
        self.is_stopped = True
