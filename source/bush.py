import pygame
import random
from source.load_image import load_image
from source.settings import BUSH_SPRITE, WINDOW_SIZE


class Bush(pygame.sprite.Sprite):
    image = load_image(BUSH_SPRITE)

    def __init__(self, bush_group):
        super().__init__(bush_group)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_SIZE[0])
        self.rect.y = -200
        while len(pygame.sprite.spritecollide(self, bush_group, False)) > 1:
            self.rect.x = random.randint(0, WINDOW_SIZE[0])

        self.is_stopped = False

    def update(self) -> None:
        if not self.is_stopped:
            self.rect.bottom += 3
            if self.rect.bottom > WINDOW_SIZE[1] + 100:
                self.kill()

    def stop(self):
        self.is_stopped = True