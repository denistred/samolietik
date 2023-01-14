import pygame
from source.settings import WOODS_MENU_BUTTON
from source.load_image import load_image


class WoodsButton(pygame.sprite.Sprite):
    image = load_image(WOODS_MENU_BUTTON)

    def __init__(self, button_group):
        super().__init__(button_group)
        self.rect = self.image.get_rect()
        self.rect.bottom = 300
        self.rect.left = 125
