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

game_fon = pygame.transform.scale(load_image('fon_1.png'), (WIDTH, HEIGHT))
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
                    Enemy('ufo.png', random.randint(0, WIDTH), random.randint(0, HEIGHT))

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
                    Bullet(player.rect.centerx, player.rect.centery, event.pos[0], event.pos[1])

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    player.speed += 10
                if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                    player.speed -= 10





        if do_draw:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - player.rect.x, mouse_y - player.rect.y
            angle = math.atan2(rel_y, rel_x)
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            player.image = pygame.transform.rotate(player.original_image, int(angle) + 20)
            player.rect = player.image.get_rect(center=(player.rect.center))
            if up_m:
                if player.rect.y - 10 >= 0:
                    player.rect.y -= player.speed

            if down_m:
                if player.rect.y + 10 + tile_height <= HEIGHT:
                    player.rect.y += player.speed
            if right_m:
                if player.rect.x + 10 + tile_width <= WIDTH:
                    player.rect.x += player.speed
            if left_m:
                if player.rect.x - 10 >= 0:
                    player.rect.x -= player.speed




            screen.blit(game_fon, (0, 0))

            col = pygame.sprite.spritecollide(player, enemy_sprites, False)
            if col:
                player.health -= 10
                col[0].kill()
                Enemy('ufo.png', random.randint(0, WIDTH), random.randint(0, HEIGHT))
            if player.health <= 0:
                player.kill()
                terminate()
            for i in bullet_sprites:
                i.move_towards()
                enemy = pygame.sprite.spritecollide(i, enemy_sprites, False)
                if enemy:
                    enemy[0].health -= 20
                    i.kill()
            for i in enemy_sprites:
                i.time += i.clock.tick()
                if i.time >= i.delay * 2:
                    i.move_towards_player(player)
                    i.time = 0
                if i.health <= 0:
                    i.kill()
                    player.kills += 1
                    Enemy('ufo.png', random.randint(0, WIDTH), random.randint(0, HEIGHT))
            all_sprites.draw(screen)
            bullet_sprites.draw(screen)
            enemy_sprites.draw(screen)
            player_group.draw(screen)
            font = pygame.font.Font(None, 50)
            text = font.render(f'Здоровье: {player.health} Убито:{player.kills}', True, (100, 255, 100))

            screen.blit(text, (20, 0))

        pygame.display.flip()
        clock.tick(FPS - 35)








class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('man.jpg')
        self.health = 2000
        self.kills = 0
        self.speed = 10
        self.original_image = pygame.transform.scale(load_image('man.jpg', -1), (tile_width, tile_height))
        self.original_image = pygame.transform.scale(self.original_image, (tile_width, tile_height))

        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.collected = 0
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()
        self.image = pygame.transform.rotate(self.image, int(45))
        self.rect = self.image.get_rect(center=(self.rect.center))

    def update(self):
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(bullet_sprites)
        self.image = load_image('bomb.png', -1)
        self.image = pygame.transform.scale(self.image, (tile_width / 4, tile_height / 4))
        self.collected = 0
        self.rect = self.image.get_rect().move(x, y)
        self.speed = 7
        self.target_x = target_x
        self.target_y = target_y
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()

    def move_towards(self):
        # print(math.sqrt(abs(self.rect.x- self.target_x) + abs(self.rect.y - self.target_y)))
        dx, dy = self.target_x - self.rect.x, self.target_y - self.rect.y
        dist = math.hypot(dx, dy)
        if round(dist, -1) != 0:
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
        self.delay = 2
        self.health = 100
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
