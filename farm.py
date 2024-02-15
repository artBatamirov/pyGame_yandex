import pygame
import sys, os

FPS = 30
pygame.init()
size = WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode(size)
copy = screen.copy()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player = None
XM, YM = 0, 0


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


def start_screen():
    xv, yv = 200, 150
    xm, ym = 0, 0
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
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN and not do_draw:
                do_draw = True
                player, level_x, level_y = generate_level(load_level('map.txt'))
                level = load_level('map.txt')
                up_m = False
                down_m = False
                right_m = False
                left_m = False
                # xv = x0 * tile_width
                # yv = y0 * tile_height
                # player.rect.x = 0
                # player.rect.y = 0
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

        if do_draw:
            if up_m:
                player.rect.y -= 10
                yv -= 10
                ym -= 1

            if down_m:
                player.rect.y += 10
                yv += 10
                ym += 1
            if right_m:
                player.rect.x -= 10
                xv += 10
                xm += 1
            if left_m:
                player.rect.x -= 10
                xv -= 10
                xm -= 1
            screen.fill((0, 0, 0))
            player.rect.x = xv + 15
            player.rect.y = yv + 5
            all_sprites.draw(screen)
            # tiles_group.draw(screen)
            # player_group.draw(screen)
            # print((xv, player.rect.x - 15), (yv, player.rect.y - 5))
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50
player  = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)



def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            # elif level[y][x] == '@':
            #     Tile('empty', x, y)
            #     new_player = Player(x, y)
            #     x0, y0 = x, y

    x, y = 200, 150
    new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

start_screen()