import math

import pygame
import os
import sys

PLAYER_SPRITE = 'player_plane.png'
PLAYER_ANIMATION = 'player_animation.png'
PLAYER_ANIMATION_COLUMNS = 4
PLAYER_ANIMATION_ROWS = 1
WINDOW_SIZE = (800, 800)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class PlayerAnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, all_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.Surface([10, 10])
        # self.image.fill((100,100,100))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(0, 0, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.top -= 10


class Player(PlayerAnimatedSprite):
    image = load_image(PLAYER_SPRITE)
    MAX_SPEED = 10

    def __init__(self, sheet, columns, rows, x, y, acceleration, bullet_count, all_sprites):
        super().__init__(sheet, columns, rows, x, y, all_sprites)
        self.all_sprites = all_sprites
        # self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.bottom = WINDOW_SIZE[1] - 50
        self.rect.centerx = WINDOW_SIZE[0] // 2

        self.acceleration = acceleration
        self.bullet_count = bullet_count
        self.velocity = [0, 0]

    def shoot(self):
        if self.bullet_count > 0:
            self.bullet_count -= 1
            Bullet(self.rect.x, self.rect.y, self.all_sprites)
            print('shoot ')

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
            self.velocity[0] = 0
        elif self.rect.x < 0:
            self.rect.x = 0
            self.velocity[0] = 0

    def move(self):
        # print(self.velocity[0])
        self.rect.right += self.velocity[0]
        self.check_position()
        # self.auto_acceleration_stop()


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
        if ev_type == pygame.KEYUP and key[pygame.K_a]:
            self.player_key = 1
        if ev_type == pygame.KEYUP and key[pygame.K_d]:
            self.player_key = 0
        if ev_type == pygame.KEYUP and not key[pygame.K_a] and not key[pygame.K_d]:
            self.player_key = None
        if ev_type == pygame.KEYDOWN and key[pygame.K_SPACE]:
            self.player.shoot()

    def start_game(self):
        self.player = Player(sheet=load_image(PLAYER_ANIMATION), columns=PLAYER_ANIMATION_COLUMNS,
                             rows=PLAYER_ANIMATION_ROWS, x=50, y=50, acceleration=(0.5, 0.5),
                             bullet_count=50, all_sprites=self.all_sprites)
        self.all_sprites.add(self.player)

    def render(self):
        self.screen.fill(pygame.Color(255, 255, 255))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

    def player_physic(self):
        # print(self.player_key)
        if self.player_key == 0:
            self.player.accelerate_right()
        elif self.player_key == 1:
            self.player.accelerate_left()
        else:
            self.player.auto_acceleration_stop()
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
