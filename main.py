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

    def __init__(self, velocity, bullet_count):
        super().__init__()
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.bottom = WINDOW_SIZE[1] - 50
        self.rect.centerx = WINDOW_SIZE[0] // 2
        self.velocity = velocity
        self.bullet_count = bullet_count

    def move_right(self):
        self.rect.right += self.velocity[0]

    def move_left(self):
        self.rect.right -= self.velocity[0]


class Game:
    def __init__(self, screen):
        self.all_sprites = pygame.sprite.Group()
        self.screen = screen

    def keys_handler(self, key):
        if key[pygame.K_d]:
            self.player.move_right()
        if key[pygame.K_a]:
            self.player.move_left()


    def start_game(self):
        self.player = Player((20, 20), 50)
        self.all_sprites.add(self.player)

    def render(self):
        self.screen.fill(pygame.Color(255, 255, 255))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)



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
            game.keys_handler(key)

        game.render()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
