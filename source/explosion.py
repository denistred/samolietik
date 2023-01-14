import pygame
from source.animated_sprite import AnimatedSprite


class Explosion(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, spawn_x, spawn_y, explosion_group):
        super().__init__(sheet, columns, rows, x, y, explosion_group)
        self.rect = self.image.get_rect()
        self.rect.centerx = spawn_x
        self.rect.centery = spawn_y

    def update(self):
        super().update()
        if self.cur_frame == len(self.frames) - 1:
            self.kill()