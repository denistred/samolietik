import pygame

from source.settings import WINDOW_SIZE, FPS
from source.menu_buttons import WoodsButton, DesertButton
from source.db_handler import Handler
from source.level import Levels


class Game:
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.button_group = pygame.sprite.Group()
        self.woods_button = WoodsButton(self.button_group)
        self.desert_button = DesertButton(self.button_group)

        self.check_player_alive_clock = pygame.time.Clock()
        self.check_player_alive_tick = 0

        self.db_handler = Handler()

        self.level = None

    def draw_score_text(self):
        max_score_woods = self.db_handler.get_score(0)
        max_score_desert = self.db_handler.get_score(1)
        font = pygame.font.Font(None, 36)
        text = font.render(f'Max score: {max_score_woods}', True, (255, 255, 255))
        self.screen.blit(text, (140, 250))
        text = font.render(f'Max score: {max_score_desert}', True, (255, 255, 255))
        self.screen.blit(text, (140, 550))

    def draw_end_screen(self):
        pygame.draw.rect(self.screen, (160, 160, 160), (100, 200, 300, 100))

        font = pygame.font.Font(None, 36)
        text = font.render(f'Your score: {self.level.score}', True, (255, 255, 255))
        self.screen.blit(text, (170, 240))

    def keys_handler(self, key, ev_type):
        if ev_type == pygame.MOUSEBUTTONDOWN and not self.level:
            self.check_position(pygame.mouse.get_pos())
        if self.level:
            self.level.keys_handler(key, ev_type)

    def check_position(self, point):
        if self.woods_button.rect.collidepoint(point):
            self.level = Levels(self.screen, 0)
        elif self.desert_button.rect.collidepoint(point):
            self.level = Levels(self.screen, 1)

    def check_player_alive(self):
        if not self.level.player.alive():
            self.check_player_alive_tick += self.check_player_alive_clock.tick()
            self.draw_end_screen()
            self.level.stop_game()
            if self.check_player_alive_tick > 2000:
                self.level.clear_level()
                self.check_player_alive_tick = 0
                self.db_handler.save_result(self.level.level_id, self.level.score)
                self.level = None
        else:
            self.check_player_alive_clock.tick()

    def render(self):
        if self.level is None:
            self.screen.fill((160, 160, 160))
            self.button_group.update()
            self.button_group.draw(self.screen)
            self.draw_score_text()

        elif self.level.level_id:
            self.level.player_physic()
            self.level.enemy_spawn()
            self.level.bush_spawn()
            self.level.player_logic()
            self.level.render()
            self.check_player_alive()

        elif not self.level.level_id:
            self.level.player_physic()
            self.level.enemy_spawn()
            self.level.trees_spawn()
            self.level.player_logic()
            self.level.render()
            self.check_player_alive()


def game_cycle():
    pygame.init()

    size = WINDOW_SIZE
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


if __name__ == '__main__':
    game_cycle()
