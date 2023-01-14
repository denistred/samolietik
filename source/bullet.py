import pygame

class Bullet(pygame.sprite.Sprite):
    BULLET_COLOR = (255, 255, 51)
    BULLET_SPEED = 10

    def __init__(self, x, y, offset_x, offset_y, bullet_group):
        super().__init__(bullet_group)
        self.image = pygame.Surface([3, 10])
        pygame.draw.rect(self.image, Bullet.BULLET_COLOR, pygame.Rect(0, 0, 3, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x + offset_x
        self.rect.y = y + offset_y

    def update(self):
        self.rect.top -= Bullet.BULLET_SPEED
        if self.rect.top < -10:
            self.kill()