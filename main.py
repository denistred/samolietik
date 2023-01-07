import math

import pygame
import os
import sys

PLAYER_SPRITE = 'star.png'
WINDOW_SIZE = (800, 800)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    image = load_image(PLAYER_SPRITE)
    MAX_SPEED = 10

    def __init__(self, acceleration, bullet_count):
        super().__init__()
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.bottom = WINDOW_SIZE[1] - 50
        self.rect.centerx = WINDOW_SIZE[0] // 2

        self.acceleration = acceleration
        self.bullet_count = bullet_count
        self.velocity = [0, 0]

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
        if self.velocity[0] > 0:
            if self.velocity[0] - math.sqrt(abs(self.velocity[0])) > 0:
                self.velocity[0] -= math.sqrt(abs(self.velocity[0]))
            else:
                self.velocity[0] -= self.velocity[0]

        elif self.velocity[0] < 0:
            if self.velocity[0] + math.sqrt(abs(self.velocity[0])) < 0:
                self.velocity[0] += math.sqrt(abs(self.velocity[0]))
            else:
                self.velocity[0] -= self.velocity[0]

    def check_position(self):
        if self.rect.x > WINDOW_SIZE[0] - self.rect.width:
            self.rect.x = WINDOW_SIZE[0] - self.rect.width
        elif self.rect.x < 0:
            self.rect.x = 0
    def move(self):
        print(self.velocity[0])
        self.rect.right += self.velocity[0]
        self.check_position()
        self.auto_acceleration_stop()


class Game:
    def __init__(self, screen):
        self.all_sprites = pygame.sprite.Group()
        self.screen = screen
        self.player_key = None

    def keys_handler(self, key, ev_type):
        if key[pygame.K_d] and ev_type == pygame.KEYDOWN:
            self.player_key = 0
        if key[pygame.K_a] and ev_type == pygame.KEYDOWN:
            self.player_key = 1
        if ev_type == pygame.KEYUP and not key[pygame.K_a] and not key[pygame.K_d]:
            self.player_key = None

    def start_game(self):
        self.player = Player((5, 5), 50)
        self.all_sprites.add(self.player)

    def render(self):
        self.screen.fill(pygame.Color(255, 255, 255))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

    def player_physic(self):
        print(self.player_key)
        if self.player_key == 0:
            self.player.accelerate_right()
        elif self.player_key == 1:
            self.player.accelerate_left()
        self.player.move()


if __name__ == '__main__':
    pygame.init()

    size = width, height = WINDOW_SIZE
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    game = Game(screen)
    game.start_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            key = pygame.key.get_pressed()
            ev_type = event.type
            game.keys_handler(key, ev_type)

        game.player_physic()
        game.render()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
