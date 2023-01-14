import random

import pygame

from source.enemy_one import EnemyOne
from source.load_image import load_image
from source.settings import WINDOW_SIZE, PLAYER_ANIMATION, FPS, ENEMY_FIRST_ANIMATION, \
    PLAYER_ANIMATION_COLUMNS, PLAYER_ANIMATION_ROWS
from source.player import Player
from source.menu_buttons import WoodsButton
from source.Tree import Tree

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()





class LevelWoods:
    def __init__(self, screen):
        self.all_sprites = pygame.sprite.Group()

        self.screen = screen

        self.score = 0

        self.stop = False

        self.player_key = None
        self.player_shoot_key = None

        self.player_clock = pygame.time.Clock()
        self.current_tick = 0

        self.enemy_spawn_clock = pygame.time.Clock()
        self.enemy_spawn_tick = 0
        self.enemy_spawn_max_tick = 250
        self.enemy_speed = 6

        self.trees_spawn_clock = pygame.time.Clock()
        self.trees_spawn_tick = 0
        self.start_game()
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
                             bullet_count=100, player_group=player_group, bullet_group=bullet_group)
        self.all_sprites.add(self.player)
        Tree(tree_group)

    def draw_bottom_gui(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, (160, 160, 160), (0, WINDOW_SIZE[1] - 50, WINDOW_SIZE[0], 50))
        font = pygame.font.Font(None, 36)
        bullet_count_text = font.render(f'Bullet count: {self.player.bullet_count}', True,
                                        (255, 255, 255))
        screen.blit(bullet_count_text, (0, WINDOW_SIZE[1] - 36))

        score_text = font.render(f'Scroe: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (250, WINDOW_SIZE[1] - 36))

    def enemy_spawn(self):
        if not self.stop:
            self.enemy_spawn_tick += self.enemy_spawn_clock.tick()
            if self.enemy_spawn_tick > self.enemy_spawn_max_tick:
                enemy_x = random.randint(20, WINDOW_SIZE[0] - 20)
                EnemyOne(load_image(ENEMY_FIRST_ANIMATION), 4, 1, 50, 50, enemy_x, self.enemy_speed,
                         enemy_group, explosion_group, bonus_group)
                self.enemy_spawn_tick = 0
                if self.enemy_spawn_max_tick > 70:
                    self.enemy_spawn_max_tick -= 0.5
                if self.enemy_speed < 11:
                    self.enemy_speed += 0.01

                if not self.stop:
                    self.score += 10
                print(self.enemy_spawn_max_tick, self.enemy_speed)

    def trees_spawn(self):
        if not self.stop:
            self.trees_spawn_tick += self.trees_spawn_clock.tick()
            if self.trees_spawn_tick > 100:
                Tree(tree_group)
                self.trees_spawn_tick = 0

    def player_physic(self):
        if self.player_key == 0:
            self.player.accelerate_right()
        elif self.player_key == 1:
            self.player.accelerate_left()
        else:
            self.player.auto_acceleration_stop()

        self.player_shooting()

        self.player.move()

    def player_logic(self):
        self.player.collision_check(enemy_group)
        self.player.pick_up_bonus(bonus_group)

    def player_shooting(self):
        if self.player_shoot_key == 1:
            self.current_tick += self.player_clock.tick()
            if self.current_tick > 300:
                self.player.shoot()
                self.current_tick = 0

    def render(self):
        self.screen.fill(pygame.Color(0, 200, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        tree_group.update()
        tree_group.draw(self.screen)
        bullet_group.update()
        bullet_group.draw(self.screen)
        enemy_group.update(bullet_group)
        enemy_group.draw(self.screen)
        explosion_group.update()
        explosion_group.draw(self.screen)
        player_group.update()
        player_group.draw(self.screen)
        bonus_group.update()
        bonus_group.draw(self.screen)
        self.draw_bottom_gui(self.screen)
        if self.stop:
            for bonus in bonus_group:
                bonus.stop()
            for tree in tree_group:
                tree.stop()
            for enemy in enemy_group:
                enemy.stop()
            self.player.stop()

    def stop_game(self):
        self.stop = True

    def clear_level(self):
        for enemy in enemy_group:
            enemy.kill()
        for tree in tree_group:
            tree.kill()
        for bonus in bonus_group:
            bonus.kill()
        for bullet in bullet_group:
            bullet.kill()


class Game:
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.button_group = pygame.sprite.Group()
        self.woods_button = WoodsButton(self.button_group)

        self.check_player_alive_clock = pygame.time.Clock()
        self.check_player_alive_tick = 0

        self.max_score = 0

        self.level = None

    def draw_score_text(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Max score: {self.max_score}', True, (255, 255, 255))
        self.screen.blit(text, (140, 250))

    def draw_end_screen(self):
        pygame.draw.rect(self.screen, (160, 160, 160), (100, 200, 300, 100))

        font = pygame.font.Font(None, 36)
        text = font.render(f'Your score: {self.level.score}', True, (255, 255, 255))
        self.screen.blit(text, (170, 240))

    def keys_handler(self, key, ev_type):
        if ev_type == pygame.MOUSEBUTTONDOWN and not self.level:
            self.check_position(pygame.mouse.get_pos())
        if self.level.__class__.__name__ == 'LevelWoods':
            self.level.keys_handler(key, ev_type)

    def check_position(self, point):
        if self.woods_button.rect.collidepoint(point):
            self.level = LevelWoods(self.screen)

    def check_player_alive(self):
        if not self.level.player.alive():
            self.check_player_alive_tick += self.check_player_alive_clock.tick()
            self.draw_end_screen()
            self.level.stop_game()
            if self.check_player_alive_tick > 2000:
                self.level.clear_level()
                self.check_player_alive_tick = 0
                self.level = None
        else:
            self.check_player_alive_clock.tick()


    def render(self):
        if self.level == None:
            self.screen.fill((160, 160, 160))
            self.button_group.update()
            self.button_group.draw(self.screen)
            self.draw_score_text()

        elif self.level.__class__.__name__ == 'LevelWoods':
            self.level.player_physic()
            self.level.enemy_spawn()
            self.level.trees_spawn()
            self.level.player_logic()
            self.level.render()
            self.check_player_alive()


if __name__ == '__main__':
    pygame.init()

    size = width, height = WINDOW_SIZE
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    game = Game(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            key = pygame.key.get_pressed()
            ev_type = event.type
            game.keys_handler(key, ev_type)

        game.render()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
