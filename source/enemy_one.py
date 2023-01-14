import pygame
import random
from source.load_image import load_image
from source.animated_sprite import AnimatedSprite
from source.explosion import Explosion
from source.settings import EXPLOSION_ANIMATION, ENEMY_FIRST_ANIMATION
from source.bonus_ammo import BonusBullet

class EnemyOne(AnimatedSprite):
    image = load_image(ENEMY_FIRST_ANIMATION)

    def __init__(self, sheet, columns, rows, x, y, spawn_x, speed, enemy_group, explosion_group, bonus_group):
        super().__init__(sheet, columns, rows, x, y, enemy_group)
        self.rect = self.image.get_rect()
        self.rect.bottom = -50
        self.rect.centerx = spawn_x
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

        self.explosion_group = explosion_group
        self.bonus_group = bonus_group

        self.is_stopped = False

    def destroy(self, bullet_group):
        for bullet in bullet_group:
            if pygame.sprite.collide_mask(self, bullet):
                self.kill()
                bullet.kill()
                Explosion(load_image(EXPLOSION_ANIMATION), 12, 1, 50, 50, self.rect.centerx,
                          self.rect.centery, self.explosion_group)
                chance = random.randint(1, 10)
                if chance == 1:
                    BonusBullet(self.rect.centerx, self.rect.centery, self.bonus_group)
                break

    def update(self, bullet_group):
        super().update()
        if not self.is_stopped:
            self.rect.bottom += self.speed
        if self.rect.bottom > 800:
            self.kill()
        self.destroy(bullet_group)

    def stop(self):
        self.is_stopped = True