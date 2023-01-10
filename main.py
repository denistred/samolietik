import math
import random

import pygame
import os
import sys

FPS = 60
WINDOW_SIZE = (500, 800)

PLAYER_SPRITE = 'player_plane.png'
PLAYER_ANIMATION = 'player_animation.png'
PLAYER_ANIMATION_COLUMNS = 4
PLAYER_ANIMATION_ROWS = 1
ENEMY_FIRST_ANIMATION = 'GER_He111_animation.png'

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
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


class EnemyFirst(AnimatedSprite):
    image = load_image('GER_He111_animation.png')

    def __init__(self, sheet, columns, rows, x, y, spawn_x, speed):
        super().__init__(sheet, columns, rows, x, y, enemy_group)
        self.rect = self.image.get_rect()
        self.rect.bottom = -50
        self.rect.centerx = spawn_x
        self.speed = speed

    def shoot(self):
        Bullet(self.rect.x, self.rect.y, 19, 15)
        Bullet(self.rect.x, self.rect.y, 47, 15)

    def destroy(self):
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.kill()

    def update(self):
        super().update()
        self.rect.bottom += self.speed
        self.destroy()


class Bullet(pygame.sprite.Sprite):
    BULLET_COLOR = (255, 255, 51)
    BULLET_SPEED = 10

    def __init__(self, x, y, offset_x, offset_y):
        super().__init__(bullet_group)
        self.image = pygame.Surface([3, 10])
        pygame.draw.rect(self.image, Bullet.BULLET_COLOR, pygame.Rect(0, 0, 3, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x + offset_x
        self.rect.y = y + offset_y

    def update(self):
        self.rect.top -= Bullet.BULLET_SPEED


class Player(AnimatedSprite):
    image = load_image(PLAYER_SPRITE)
    MAX_SPEED = 10

    def __init__(self, sheet, columns, rows, x, y, acceleration, bullet_count, all_sprites):
        super().__init__(sheet, columns, rows, x, y, player_group)
        self.all_sprites = all_sprites
        self.rect = self.image.get_rect()
        self.rect.bottom = WINDOW_SIZE[1] - 50
        self.rect.centerx = WINDOW_SIZE[0] // 2

        self.acceleration = acceleration
        self.bullet_count = bullet_count
        self.velocity = [0, 0]

    def shoot(self):
        if self.bullet_count > 0:
            self.bullet_count -= 1
            Bullet(self.rect.x, self.rect.y, 19, 15)
            Bullet(self.rect.x, self.rect.y, 47, 15)
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

    def collision_check(self):
        if pygame.sprite.spritecollide(self, enemy_group, True):
            sys.exit(0)

    def move(self):
        self.rect.right += self.velocity[0]
        self.check_position()
        self.collision_check()


class Game:
    def __init__(self, screen):
        self.all_sprites = pygame.sprite.Group()

        self.screen = screen

        self.player_key = None
        self.player_shoot_key = None

        self.player_clock = pygame.time.Clock()
        self.current_tick = 0

        self.enemy_spawn_clock = pygame.time.Clock()
        self.enemy_spawn_tick = 0

        self.enemy_spawn()

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
        if key[pygame.K_SPACE] and ev_type == pygame.KEYDOWN:
            self.player_shoot_key = 1
        if not key[pygame.K_SPACE] and ev_type == pygame.KEYUP:
            self.player_shoot_key = None

    def start_game(self):
        self.player = Player(sheet=load_image(PLAYER_ANIMATION), columns=PLAYER_ANIMATION_COLUMNS,
                             rows=PLAYER_ANIMATION_ROWS, x=50, y=50, acceleration=(0.5, 0.5),
                             bullet_count=100, all_sprites=self.all_sprites)
        self.all_sprites.add(self.player)
        # EnemyFirst(load_image(ENEMY_FIRST_ANIMATION), 4, 1, 50, 50, 100, 6, self.all_sprites)

    def enemy_spawn(self):
        self.enemy_spawn_tick += self.enemy_spawn_clock.tick()
        enemy_spawn_max_tick = random.randint(250, 750)
        if self.enemy_spawn_tick > enemy_spawn_max_tick:
            enemy_x = random.randint(20, WINDOW_SIZE[0] - 20)
            EnemyFirst(load_image(ENEMY_FIRST_ANIMATION), 4, 1, 50, 50, enemy_x, 6)
            self.enemy_spawn_tick = 0

    def render(self):
        self.screen.fill(pygame.Color(0, 200, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        bullet_group.update()
        bullet_group.draw(self.screen)
        enemy_group.update()
        enemy_group.draw(self.screen)
        player_group.update()
        player_group.draw(self.screen)

    def player_physic(self):
        # print(self.player_key)
        if self.player_key == 0:
            self.player.accelerate_right()
        elif self.player_key == 1:
            self.player.accelerate_left()
        else:
            self.player.auto_acceleration_stop()

        if self.player_shoot_key == 1:
            self.current_tick += self.player_clock.tick()
            if self.current_tick > 300:
                self.player.shoot()
                self.current_tick = 0

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
        game.enemy_spawn()
        game.render()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
