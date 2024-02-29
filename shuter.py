import random

import pygame
import sys, os
import math
import pygame_widgets
from pygame_widgets.button import Button

FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(size)
copy = screen.copy()
clock = pygame.time.Clock()
wave_clock = pygame.time.Clock()
wave_time = wave_clock.tick()
all_sprites = pygame.sprite.Group()
need_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
top_x, top_y = 20, 0
do_stop = False
player0 = None
do_draw = False
XM, YM = 0, 0
tile_width = tile_height = 50


class Camera():
    def __init__(self):
        self.on = True

    def move(self, x, y):
        if self.on:
            for i in all_sprites:
                i.rect.x -= x
                i.rect.y -= y


cam = Camera()


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


# game_fon = pygame.transform.scale(load_image('fon_1.png'), (WIDTH, HEIGHT))


def terminate():
    font = pygame.font.Font(None, 50)
    text = font.render('Game Over', True, (100, 255, 100))
    pygame_widgets.update(pygame.event.get())
    screen.blit(text, (50, 50))
    do_draw = False
    clock.tick(30)
    pygame.quit()
    sys.exit()


def start_screen():
    global wave_time
    global do_draw
    global player0
    global do_stop
    # xm, ym = 0, 0
    tab = 0
    wave_number = 0
    do_draw = False
    button = Button(screen, 750, 10, 30, 30, text='Stop', fontSize=10, margin=20, inactiveColour=(200, 50, 0),
                    hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), radius=20, onClick=stop)
    while True:
        if not do_draw:
            intro_text = ["Новая игра", "Продолжить игру", "Результаты"]

            fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for i in range(len(intro_text)):
                string_rendered = font.render(intro_text[i], 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                if i == tab:
                    pygame.draw.rect(screen, (144, 238, 144),
                                     (
                                     intro_rect.x - 5, intro_rect.y - 5, intro_rect.width + 10, intro_rect.height + 10))
                screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            tic = clock.tick()
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                do_draw = False
                if tab == 0 or tab == 1 and all_sprites.sprites():
                    stop(player, wave_number)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                print(event.mod, pygame.KMOD_LSHIFT)
                if (event.mod == 4097):

                    tab -= 1
                else:
                    tab += 1
                tab %= 3
            elif (event.type == pygame.MOUSEBUTTONDOWN) and not do_draw:
                do_draw = True
                if tab == 0:
                    # xm = player.rect.x // tile_width
                    # ym = player.rect.y // tile_height
                    player = generate_level(load_level('maps\loc2.txt'))
                    do_count = True
                    player0 = player
                    wave_clock.tick()
                    do_stop = False
                if tab == 1:
                    do_stop = False
                    with open('data/result/save.txt', mode='r') as f1:
                        inf = f1.readlines()

                        for i in inf:
                            print(i)
                            sprite = i.strip('\n').split()
                            if sprite[2] == 'Player':
                                player = Player(int(sprite[0]), int(sprite[1]))
                                print(11111111)
                                with open('data/result/result.txt', mode='r') as f2:
                                    inf = f2.readline(-1).split()
                                    player.health == int(inf[0])
                                    player.kills == int(inf[1])
                                    player.coins == int(inf[2])
                                    wave_number == int(inf[3])
                            elif sprite[2] == 'Enemy':
                                Enemy(int(sprite[0]), int(sprite[1]), wave_number)
                    do_count = True
                    player0 = player
                    wave_clock.tick()






            if do_draw and not do_stop and tab in (0, 1):

                if event.type == pygame.MOUSEBUTTONDOWN:
                    Bullet(player.rect.centerx, player.rect.centery, event.pos[0], event.pos[1], 250)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    player.speed += 5
                if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                    player.speed -= 5

        key_pressed_is = pygame.key.get_pressed()

        if do_draw and not do_stop and tab in (0, 1):
            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # rel_x, rel_y = mouse_x - player.rect.x, mouse_y - player.rect.y
            # angle = math.atan2(rel_y, rel_x)
            # angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            # player.image = pygame.transform.rotate(player.original_image, int(angle) + 20)
            # player.rect = player.image.get_rect(center=(player.rect.center))
            if key_pressed_is[pygame.K_w]:
                if player.rect.y >= 0:
                    player.rect.y -= player.speed
                    if pygame.sprite.spritecollide(player, tiles_group, False):
                        player.rect.y += player.speed
                    # else:
                    #     cam.move(0, -player.speed)
            if key_pressed_is[pygame.K_s]:
                if player.rect.y + player.speed <= HEIGHT:
                    player.rect.y += player.speed
                    if pygame.sprite.spritecollide(player, tiles_group, False):
                        player.rect.y -= player.speed
                    # else:
                    #     cam.move(0, player.speed)
            if key_pressed_is[pygame.K_d]:
                if player.rect.x + player.speed <= WIDTH:
                    player.rect.x += player.speed
                    if pygame.sprite.spritecollide(player, tiles_group, False):
                        player.rect.x -= player.speed
                    # else:
                    #     cam.move(player.speed, 0)
            if key_pressed_is[pygame.K_a]:
                if player.rect.x >= 0:
                    player.rect.x -= player.speed
                    if pygame.sprite.spritecollide(player, tiles_group, False):
                        player.rect.x += player.speed
                    # else:
                    #     cam.move(-player.speed, 0)

            # screen.blit(game_fon, (0, 0))
            screen.fill((240, 240, 240))
            # if player.rect.x >= 780:
            #     for spr in all_sprites:
            #         spr.rect.x -= 100
            # if player.rect.x <= 20:
            #     for spr in all_sprites:
            #         spr.rect.x += 100
            col = pygame.sprite.spritecollide(player, enemy_sprites, False)
            if col:
                player.health -= col[0].damage
                col[0].kill()
                if not enemy_sprites.sprites():
                    do_count = True
                    wave_number += 1
                    wave_clock.tick()
            if player.health <= 0:
                player.kill()
                stop()
                terminate()
            for i in bullet_sprites:
                i.move_towards()
                enemy = pygame.sprite.spritecollide(i, enemy_sprites, False)
                tile = pygame.sprite.spritecollide(i, tiles_group, False)
                if tile:
                    i.kill()
                if enemy:
                    enemy[0].health -= 50
                    i.kill()
            # if not enemy_sprites.sprites():
            #     do_count = True
            #     print(do_count, enemy_sprites.sprites())
            for i in enemy_sprites:
                i.delay -= 1
                i.time += i.clock.tick()
                i.change_direct(player)
                if i.delay == 0:
                    i.delay = 5
                    i.update()
                if i.time >= i.delay * 2:
                    i.move_towards_player(player)
                    i.time = 0
                if i.health <= 0:
                    i.kill()
                    x_e = i.rect.x
                    y_e = i.rect.y
                    if not enemy_sprites.sprites():
                        do_count = True
                        wave_number += 1
                        wave_clock.tick()
                    for el in range(i.cost):
                        Coin(random.randint(x_e - 10, x_e + 10), random.randint(y_e - 10, y_e + 10))
                    player.kills += 1
                    # Enemy( random.randint(0, WIDTH), random.randint(0, HEIGHT))
            coin = pygame.sprite.spritecollide(player, coin_sprites, False)
            if coin:
                coin[0].kill()
                if coin[0].inf == 'coin.jpg':
                    player.coins += 1
                elif coin[0].inf == 'heart.jpg':
                    player.health += 5
                    if player.health > 200:
                        player.health = 200

            # need_group.empty()
            # for spr in all_sprites:
            #     if math.sqrt(abs(spr.rect.x - player.rect.x) ** 2 + abs(spr.rect.y - player.rect.y) ** 2) <= w
            #         need_group.add(spr)
            all_sprites.draw(screen)
            # need_group.draw(screen)
            bullet_sprites.draw(screen)
            enemy_sprites.draw(screen)
            player_group.draw(screen)
            font = pygame.font.Font(None, 35)
            if do_count:
                wave_time += wave_clock.tick()
                screen.blit(font.render(f'Сдедующая волна через: {10 - wave_time // 1000}', 1, pygame.Color('red')), (20, 40))
            if wave_time // 1000 >= 10 and not enemy_sprites.sprites():
                wave_time = 0
                do_count = False
                for i in range(5 + wave_number // 2):
                    x, y = random.randint(0, WIDTH // 50), random.randint(0, HEIGHT // 50)
                    while math.sqrt(abs(x - player.rect.x) ** 2 + abs(y - player.rect.y) ** 2) < 100:
                        x, y = random.randint(0, WIDTH // 50), random.randint(0, HEIGHT // 50)
                    Enemy(x * 50, y * 50, wave_number)

            text = font.render(
                f'Здоровье: {player.health}    Убито:{player.kills}     Монеты:{player.coins}    Волна: {wave_number}', True,
                pygame.Color('black'))
            pygame_widgets.update(pygame.event.get())
            screen.blit(text, (20, 0))
        # if do_stop:
        #     tab = 0
        #     intro_text = ["Продолжить", "Меню", "Настройки"]
        #     font = pygame.font.Font(None, 50)
        #     text_coord = 200
        #     for i in range(len(intro_text)):
        #         string_rendered = font.render(intro_text[i], 1, pygame.Color('white'))
        #         intro_rect = string_rendered.get_rect()
        #         text_coord += 10
        #         intro_rect.top = text_coord
        #         intro_rect.x = 10
        #         text_coord += intro_rect.height
        #         if i == tab:
        #             pygame.draw.rect(screen, (144, 238, 144),
        #                              (
        #                                  intro_rect.x - 5, intro_rect.y - 5, intro_rect.width + 10,
        #                                  intro_rect.height + 10))
        #         screen.blit(string_rendered, intro_rect)
        if tab == 2 and do_draw:
            screen.fill((255, 255, 255))
            with open('data/result/result.txt', mode='r') as file:
                result = file.readlines()
                screen.blit(font.render('Результаты игры', 1, pygame.Color('black')), (20, 20))
                screen.blit(font.render('Здоровье', 1, pygame.Color('black')), (20, 50))
                screen.blit(font.render('Убийства', 1, pygame.Color('black')), (140, 50))
                screen.blit(font.render('Монеты', 1, pygame.Color('black')), (260, 50))
                screen.blit(font.render('Волны', 1, pygame.Color('black')), (380, 50))

                text_coord = 100
                for i in result:
                    text = i.strip('\n').split()
                    pygame.draw.line(screen, (0,0, 0), (20, text_coord - 2), (450, text_coord - 2))
                    screen.blit(font.render(text[0], 1, pygame.Color('black')), (40, text_coord))
                    screen.blit(font.render(text[1], 1, pygame.Color('black')), (160, text_coord))
                    screen.blit(font.render(text[2], 1, pygame.Color('black')), (280, text_coord))
                    screen.blit(font.render(text[3], 1, pygame.Color('black')), (400, text_coord))
                    # string_rendered = font.render(text, 1, pygame.Color('black'))
                    # intro_rect = string_rendered.get_rect()
                    text_coord += 20
                    # intro_rect.top = text_coord
                    # intro_rect.left = 100
                    # intro_rect.x = 10
                    # text_coord += intro_rect.height
                    # screen.blit(string_rendered, intro_rect)
                pygame.draw.line(screen, (0, 0, 0), (20, text_coord -2), (450, text_coord -2))

        pygame.display.flip()
        clock.tick(FPS - 35)


def stop(player, wave_number):
    global do_stop
    do_stop = True
    do_draw = False
    with open('data/result/result.txt', mode='a') as output:
        output.write(f'\n{player.health} {player.kills} {player.coins} {wave_number}')
    with open('data/result/save.txt', mode='w') as f:
        for sprite in all_sprites:
            f.write(f'{sprite.rect.x} {sprite.rect.y} {sprite.__class__.__name__}\n')
            sprite.kill()


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            # if level[y][x] == '#':
            #     Tile('wall', x, y)
            if level[y][x] == 'c':
                Coin(top_x + x * 50, top_y + y * 50, 25)
            if level[y][x] == '@':
                player = Player(top_x + x * 50, top_y + y * 50)
    x, y = 12, 4
    # for i in range(8):
    #     Tile('wall', x, y)
    #     Tile('wall', x, y + 3)
    #     x += 1

    return player


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('man.jpg', -1)
        self.health = 200
        self.kills = 0
        self.speed = 10
        self.coins = 0
        self.original_image = pygame.transform.scale(load_image('man.jpg', -1), (tile_width, tile_height))
        self.original_image = pygame.transform.scale(self.original_image, (tile_width - 15, tile_height - 15))

        self.image = pygame.transform.scale(self.image, (tile_width - 15, tile_height - 15))
        self.collected = 0
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()
        # self.image = pygame.transform.rotate(self.image, int(45))
        # self.rect = self.image.get_rect(center=(self.rect.center))

    def update(self):
        pass


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, distance):
        super().__init__(bullet_sprites)
        self.image = load_image('bomb.png', -1)
        self.image = pygame.transform.scale(self.image, (tile_width / 4, tile_height / 4))
        self.collected = 0
        self.rect = self.image.get_rect().move(x, y)
        self.speed = 7

        self.distance = distance
        self.target_x = target_x
        self.target_y = target_y
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()
        dx, dy = self.target_x - self.rect.x, self.target_y - self.rect.y
        self.old_dist = math.hypot(dx, dy)

    def move_towards(self):
        # print(math.sqrt(abs(self.rect.x- self.target_x) + abs(self.rect.y - self.target_y)))
        dx, dy = self.target_x - self.rect.x, self.target_y - self.rect.y
        self.dist = math.hypot(dx, dy)
        if self.old_dist - self.dist >= self.distance:
            self.kill()
        if round(self.dist, -1) != 0:

            dx, dy = dx / self.dist, dy / self.dist  # Normalize.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        else:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, difficulty):
        super().__init__(enemy_sprites, all_sprites)
        self.clock = pygame.time.Clock()
        self.direct = 'l'
        self.num = 0
        self.damage = random.randint(4, 8)
        self.speed = random.randint(5, 8)
        self.delay = 5
        self.cost = random.randint(1, 2)
        self.health = random.randint(50 + difficulty // 2, 100 + difficulty // 2)
        self.time = self.clock.tick()
        self.image = load_image(f'Individual Sprites/slime-move-{self.num}.png')
        self.scale = random.randint(tile_width - 15, tile_width - 15 + difficulty * 2)
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.num += 1
        self.num %= 4
        self.image = load_image(f'Individual Sprites/slime-move-{self.num}.png')
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        if self.direct == 'r':
            self.image = pygame.transform.flip(self.image, True, False)

    def change_direct(self, player):
        # print(self.direct, self.rect.x > player.rect.x)
        if self.rect.x < player.rect.x and self.direct == 'l':
            self.direct = 'r'
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.x >= player.rect.x and self.direct == 'r':
            self.direct = 'l'
            self.image = pygame.transform.flip(self.image, True, False)

    def move_towards_player(self, player):
        # # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        print(dist)
        if dist <= 60:
            self.image = load_image('Individual Sprites/slime-attack-2.png')
            self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
            if self.direct == 'r':
                self.image = pygame.transform.flip(self.image, True, False)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed


            if pygame.sprite.spritecollide(self, tiles_group, False):
                self.rect.x -= dx * self.speed
                self.rect.y -= dy * self.speed



class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, size=tile_width / 3):
        super().__init__(all_sprites, coin_sprites)
        self.inf = random.choices(['coin.jpg', 'heart.jpg'],k=1, weights=[50, 10])[0]
        self.image = load_image(self.inf, -1)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect().move(x, y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


start_screen()
