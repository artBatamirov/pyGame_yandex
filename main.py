import pygame
import sys, os

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
player = None
XM, YM = 0, 0
tile_width = tile_height = 50

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, plant_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.rect = self.rect.move(x * tile_width, y * tile_height)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, frame_n=-1):
        if frame_n == -1:
            frame_n = self.cur_frame
        self.cur_frame = (frame_n + 1) % len(self.frames)
        self.image = self.frames[frame_n]
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))





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


# dragon = AnimatedSprite(load_image("Sprout Lands - Sprites - Basic pack\Objects\Basic_Plants.png"), 6, 2, 700, 700)

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
            elif (event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN) and not do_draw:
                do_draw = True
                player, level_x, level_y = generate_level(load_level('map.txt'))
                level = load_level('map.txt')
                xm = player.rect.x // tile_width ** 2
                ym = player.rect.y // tile_width ** 2


            if do_draw:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    print(level[ym - 1][xm])
                    if not(level[ym - 1][xm] == '#'):
                        player.rect.y -= 50
                        yv -= 50
                        ym -= 1
                        coll = pygame.sprite.spritecollide(player, plant_group, False)
                        print(coll)
                    if coll:
                        print('cur_frame', coll[0].cur_frame)
                        if coll[0].cur_frame == 5:
                            print(coll[0])
                            clock.tick(10)
                            # coll[0].update(5)
                            all_sprites.remove(coll[0])
                            plant_group.remove(coll[0])

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    print(level[ym + 1][xm])
                    if not(level[ym + 1][xm] == '#'):
                        player.rect.y += 50
                        yv += 50
                        ym += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    print(level[ym][xm + 1])
                    if not (level[ym][xm + 1] == '#'):
                        player.rect.x -= 50
                        xv += 50
                        xm += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    print(level[ym][xm - 1])
                    if not (level[ym][xm - 1] == '#'):
                        player.rect.x -= 50
                        xv -= 50
                        xm -= 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    AnimatedSprite(load_image("Sprout Lands - Sprites - Basic pack\Objects\Basic_Plants.png"),
                                            6, 2, xm, ym)
                    print(xm, ym)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    all_sprites.update()
        if do_draw:
            screen.fill((0, 0, 0))
            player.rect.x = xv + 15
            player.rect.y = yv + 5
            # all_sprites.update()
            all_sprites.draw(screen)
            player_group.draw(screen)
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


player  = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
    def update(self):
        pass



def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                AnimatedSprite(load_image("Sprout Lands - Sprites - Basic pack\Objects\Basic_Plants.png"), 6, 2, x, y)
                # new_player = Player(x, y)
                # x0, y0 = x, y

    x, y = 200, 150
    new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

start_screen()
