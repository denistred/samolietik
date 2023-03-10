import random
import pygame

from source.enemy_one import Enemy
from source.load_image import load_image
from source.settings import WINDOW_SIZE, PLAYER_ANIMATION, ENEMY_FIRST_ANIMATION, \
    PLAYER_ANIMATION_COLUMNS, PLAYER_ANIMATION_ROWS, ENEMY_MIN_SPAWN_TICK, ENEMY_SPAWN_TICK_CHANGE, \
    ENEMY_MAX_SPEED, ENEMY_SPEED_CHANGE, ENEMY_START_SPAWN_TICK, ENEMY_START_SPEED
from source.player import Player
from source.Tree import Tree
from source.bush import Bush

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
bush_group = pygame.sprite.Group()


class Levels:
    def __init__(self, screen, level_code):  # 0 - woods 1 - desert
        self.all_sprites = pygame.sprite.Group()
        self.screen = screen
        self.level_id = level_code

        self.score = 0

        self.stop = False

        self.player_key = None
        self.player_shoot_key = None

        self.player_clock = pygame.time.Clock()
        self.current_tick = 0

        self.enemy_spawn_clock = pygame.time.Clock()
        self.enemy_spawn_tick = 0
        self.enemy_spawn_max_tick = ENEMY_START_SPAWN_TICK
        self.enemy_speed = ENEMY_START_SPEED

        self.start_game()
        self.enemy_spawn()

        if self.level_id:
            self.desert_background()
        else:
            self.woods_background()

    def woods_background(self):
        self.trees_spawn_clock = pygame.time.Clock()
        self.trees_spawn_tick = 0

    def desert_background(self):
        self.bush_spawn_clock = pygame.time.Clock()
        self.bush_spawn_tick = 0

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
                Enemy(load_image(ENEMY_FIRST_ANIMATION), 4, 1, 50, 50, enemy_x, self.enemy_speed,
                      enemy_group, explosion_group, bonus_group)
                self.enemy_spawn_tick = 0
                if self.enemy_spawn_max_tick > ENEMY_MIN_SPAWN_TICK:
                    self.enemy_spawn_max_tick -= ENEMY_SPAWN_TICK_CHANGE
                if self.enemy_speed < ENEMY_MAX_SPEED:
                    self.enemy_speed += ENEMY_SPEED_CHANGE

                if not self.stop:
                    self.score += 10

    def trees_spawn(self):
        if not self.stop:
            self.trees_spawn_tick += self.trees_spawn_clock.tick()
            if self.trees_spawn_tick > 100:
                Tree(tree_group)
                self.trees_spawn_tick = 0

    def bush_spawn(self):
        if not self.stop:
            self.bush_spawn_tick += self.bush_spawn_clock.tick()
            if self.bush_spawn_tick > 100:
                Bush(bush_group)
                self.bush_spawn_tick = 0

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

    def stop_all_object(self):
        if self.stop:
            for bonus in bonus_group:
                bonus.stop()
            for tree in tree_group:
                tree.stop()
            for enemy in enemy_group:
                enemy.stop()
            for bush in bush_group:
                bush.stop()
            self.player.stop()
            self.stop_game()

    def render(self):
        if self.level_id:
            self.screen.fill(pygame.Color(222, 160, 44))
            bush_group.update()
            bush_group.draw(self.screen)
        else:
            self.screen.fill(pygame.Color(0, 200, 0))
            tree_group.update()
            tree_group.draw(self.screen)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
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
        self.stop_all_object()

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
        for bush in bush_group:
            bush.kill()
