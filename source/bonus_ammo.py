import pygame
from source.load_image import load_image


class BonusBullet(pygame.sprite.Sprite):
    image = load_image('bonus_bullets.png')

    def __init__(self, x, y, bonus_group):
        super().__init__(bonus_group)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.is_stopped = False

    def update(self) -> None:
        if not self.is_stopped:
            self.rect.y += 2

    def stop(self):
        self.is_stopped = True
