import random

import pygame
import sys, os
import math

FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(size)
copy = screen.copy()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player = None
XM, YM = 0, 0
tile_width = tile_height = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(enemy_sprites)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.speed = 5
        self.delay = 1000
        self.time += self.clock.tick()
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def update(self, frame_n=-1):
        if frame_n == -1:
            frame_n = self.cur_frame
        self.cur_frame = (frame_n + 1) % len(self.frames)
        self.image = self.frames[frame_n]
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))


def start_screen():
    # xm, ym = 0, 0
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    do_draw = False
    while True:
        for event in pygame.event.get():
            tic = clock.tick()
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or \
                  event.type == pygame.MOUSEBUTTONDOWN) and not do_draw:
                do_draw = True
                player = Player(100, 100)
                xm = player.rect.x // tile_width
                ym = player.rect.y // tile_height
                up_m = False
                down_m = False
                right_m = False
                left_m = False
                for i in range(5):
                    Enemy('mario.png', random.randint(0, WIDTH), random.randint(0, HEIGHT))

            if do_draw:

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                    up_m = True


                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    down_m = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    right_m = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    left_m = True

                if (event.type == pygame.KEYUP and event.key == pygame.K_w):
                    up_m = False
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    down_m = False

                if event.type == pygame.KEYUP and event.key == pygame.K_d:
                    right_m = False

                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    left_m = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    Bullet(player.rect.x, player.rect.y, event.pos[0], event.pos[1])



        if do_draw:
            if up_m:
                player.rect.y -= 10
            if down_m:
                player.rect.y += 10
            if right_m:
                player.rect.x += 10
            if left_m:
                player.rect.x -= 10



            screen.fill((200, 200, 200))
            all_sprites.draw(screen)
            for i in bullet_sprites:
                i.move_towards_player()
                if pygame.sprite.spritecollide(i, enemy_sprites, True):
                    i.kill()
            for i in enemy_sprites:
                i.time += i.clock.tick()
                if i.time >= i.delay:
                    i.move_towards_player(player)
            bullet_sprites.draw(screen)
            enemy_sprites.draw(screen)
            player_group.draw(screen)
            font = pygame.font.Font(None, 50)
            text = font.render(f'Собрано растений: {player.collected}', True, (100, 255, 100))

            screen.blit(text, (20, 0))

        pygame.display.flip()
        clock.tick(FPS - 35)







class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('ufo.png')
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.collected = 0
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()

    def update(self):
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(bullet_sprites)
        self.image = load_image('bomb.png')
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.collected = 0
        self.rect = self.image.get_rect().move(x, y)
        self.speed = 7
        self.target_x = target_x
        self.target_y = target_y
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()

    def move_towards_player(self):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = self.target_x - self.rect.x, self.target_y - self.rect.y
        dist = math.hypot(dx, dy)
        if round(dist, 0) != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        else:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(enemy_sprites)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.speed = 10
        self.delay = 1000
        self.time += self.clock.tick()
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(
            x, y)

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed


    def update(self, frame_n=-1):
        if frame_n == -1:
            frame_n = self.cur_frame
        self.cur_frame = (frame_n + 1) % len(self.frames)
        self.image = self.frames[frame_n]
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))


start_screen()
