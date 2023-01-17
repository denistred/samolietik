import pygame
import random
from source.load_image import load_image
from source.settings import TREE_SPRITE, WINDOW_SIZE


class Tree(pygame.sprite.Sprite):
    image = load_image(TREE_SPRITE)

    def __init__(self, tree_group):
        super().__init__(tree_group)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_SIZE[0])
        self.rect.y = -200
        while len(pygame.sprite.spritecollide(self, tree_group, False)) > 1:
            self.rect.x = random.randint(0, WINDOW_SIZE[0])

        self.is_stopped = False

    def update(self) -> None:
        if not self.is_stopped:
            self.rect.bottom += 3
            if self.rect.bottom > WINDOW_SIZE[1] + 100:
                self.kill()

    def stop(self):
        self.is_stopped = True
