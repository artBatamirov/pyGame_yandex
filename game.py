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
plant_group = pygame.sprite.Group()
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
                player, level_x, level_y = generate_level(load_level('map1.txt'))
                level = load_level('map1.txt')
                xm = player.rect.x // tile_width
                ym = player.rect.y // tile_height
                # if player.rect.x >= WIDTH:
                #     v = player.rect.x - WIDTH // 2 - 15
                #     for i in all_sprites:
                #         i.rect.x -= v
                up_m = False
                down_m = False
                right_m = False
                left_m = False
                # enemy = Enemy('ufo.png', 10, 15)

            if do_draw:

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                    player.rect.y -= tile_height
                    ym -= 1
                    up_m = True

                    for i in all_sprites:
                        i.rect.y += tile_height
                        if i.rect.y >= HEIGHT:
                            i.rect.y = i.rect.y - HEIGHT

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    player.rect.y += tile_height
                    ym += 1
                    # camera.dy -= tile_height
                    # print(all_sprites.sprites())
                    # if all_sprites.sprites()[-1].rect.y <= HEIGHT:
                    for i in all_sprites:
                        i.rect.y -= tile_height

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    player.rect.x += tile_width
                    xm += 1
                    # camera.dx -= tile_width
                    for i in all_sprites:
                        i.rect.x -= tile_width

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    player.rect.x -= tile_width
                    xm -= 1
                    # camera.dx += tile_width

                    for i in all_sprites:
                        i.rect.x += tile_width


        if do_draw:
            if up_m:
                player.rect.y -= tile_height
                ym -= 1
                up_m = True
                for i in all_sprites:
                    i.rect.y += tile_height
                    if i.rect.y >= HEIGHT:
                        i.rect.y = i.rect.y - HEIGHT

            screen.fill((200, 200, 200))
            all_sprites.draw(screen)
            enemy_sprites.draw(screen)
            player_group.draw(screen)
            font = pygame.font.Font(None, 50)
            text = font.render(f'Собрано растений: {player.collected}', True, (100, 255, 100))
            # enemy.time += enemy.clock.tick()
            # if enemy.time >= enemy.delay:
            #     enemy.move_towards_player(player)

            screen.blit(text, (20, 0))

        pygame.display.flip()
        clock.tick(FPS - 48)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = mapFile.read().split('\n\n')
        for i in range(len(level_map)):
            level_map[i] = level_map[i].split('\n')

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return random.choices(level_map, k=4)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'bomb': load_image('bomb.png')
}
player_image = load_image('ufo.png', -1)

player = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.collected = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()

    def update(self):
        pass


def generate_level(level):
    new_player, x, y = None, None, None
    lvl = []
    for i in level:
        lvl += i
    for y in range(len(lvl)):
        for x in range(len(lvl[y])):
            for cell in lvl[y][x]:
                if cell == '.':
                    Tile('empty', x + 4, y)
                elif cell == '#':
                    Tile('wall', x + 4, y)
                elif cell == 'F':
                    Tile('empty', x + 4, y)
                    # AnimatedSprite(load_image("Sprout Lands - Sprites - Basic pack\Objects\Basic_Plants.png"), 6, 2, x, y)

                elif cell == '@':
                    Tile('empty', x + 4, y)
                    Tile('bomb', x + 4, y)

    new_player = Player(5, 12)
    print()
    return new_player, x, y


start_screen()
