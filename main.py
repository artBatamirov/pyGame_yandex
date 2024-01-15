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
class Plant(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, plant_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 1
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delay = 10000
        self.time += self.clock.tick()
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


# class Camera:
#     def __init__(self):
#         self.dx = 0
#         self.dy = 0
#
#     def apply(self, obj):
#         obj.rect.x += self.dx
#         obj.rect.y += self.dy
#
#     def null(self):
#         dx = 0
#         dy = 0
#
#
# camera = Camera()

# class Man(pygame.sprite.Sprite):
#     def __init__(self, image, x, y):
#         super().__init__(all_sprites, player_group)
#         self.clock = pygame.time.Clock()
#         self.time = 0
#         self.delay = 10000
#         self.time += self.clock.tick()
#         self.image = load_image(image,-1)
#         self.image = pygame.transform.scale(self.image, (tile_width * 2, tile_height * 2))
#         self.rect = self.image.get_rect().move(
#             tile_width * x, tile_height * y)
#         self.rotate(-90)
#
#     def update(self, x, y):
#         self.rect.x += x
#         self.rect.y += y
#
#     def rotate(self, angle):
#         # mouse_x, mouse_y = pygame.mouse.get_pos()
#         # rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
#         # angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
#         self.image = pygame.transform.rotate(self.image, int(angle))
#         self.rect = self.image.get_rect()
#
#
# man = Man('man.jpg', 2, 5)




def terminate():
    pygame.quit()
    sys.exit()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.speed = 1
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
                player, level_x, level_y = generate_level(load_level('map.txt'))

                level = load_level('map.txt')
                xm = player.rect.x // tile_width
                ym = player.rect.y // tile_height
                if player.rect.x >= WIDTH:
                    v = player.rect.x - WIDTH  // 2 - 15
                    for i in all_sprites:
                        i.rect.x -= v
                up_m = False
                down_m = False
                right_m = False
                left_m = False
                enemy = Enemy('box.png', 0,0)




            if do_draw:
                print('up_m',up_m, 'down_m', down_m, 'right_m',right_m, 'left_m',left_m)
                if event.type == pygame.KEYUP and event.key == pygame.K_UP:

                    up_m = False
                    print(up_m)

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                    man.update(0, 10 * tic // 1000)
                    if ym -1 >= 0 and level[ym - 1][xm] != '#':
                        player.rect.y -= tile_height
                        ym -= 1
                        up_m = True

                        # camera.dy += tile_height
                        # print(all_sprites.sprites())
                        # if all_sprites.sprites()[0].rect.y < 0:
                        for i in all_sprites:
                            i.rect.y += tile_height


                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    man.update(0, -10 * tic // 1000)
                    if ym + 1 <= level_y and level[ym + 1][xm] != '#':
                        player.rect.y += tile_height
                        ym += 1
                        # camera.dy -= tile_height
                        # print(all_sprites.sprites())
                        # if all_sprites.sprites()[-1].rect.y <= HEIGHT:
                        for i in all_sprites:
                                i.rect.y -= tile_height

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if xm + 1 <= level_x and level[ym][xm + 1] != '#':
                        player.rect.x += tile_width
                        xm += 1
                        # camera.dx -= tile_width
                        for i in all_sprites:
                            i.rect.x -= tile_width

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if xm - 1 >= 0 and level[ym][xm - 1] != '#':
                        player.rect.x -= tile_width
                        xm -= 1
                        # camera.dx += tile_width

                        for i in all_sprites:
                             i.rect.x += tile_width

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    Plant(load_image("Sprout Lands - Sprites - Basic pack\Objects\Basic_Plants.png"),
                                            6, 2, player.rect.x // tile_width, player.rect.y // tile_height)
                    print(xm, ym)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    flower = pygame.sprite.spritecollide(player, plant_group, False)
                    if flower:
                        flower[0].delay //= 2



                flower = pygame.sprite.spritecollide(player, plant_group, False)
                if flower:
                    if flower[0].cur_frame == 5:
                        all_sprites.remove(flower[0])
                        plant_group.remove(flower[0])
                        player.collected += 1


        if do_draw:
            if not pygame.event.get():
                if up_m:
                    if ym - 1 >= 0 and level[ym - 1][xm] != '#':
                        player.rect.y -= tile_height
                        ym -= 1
                        up_m = True
                        for i in all_sprites:
                            i.rect.y += tile_height
                if down_m:
                    if ym + 1 <= level_y and level[ym + 1][xm] != '#':
                        player.rect.y += tile_height
                        ym += 1
                        for i in all_sprites:
                            i.rect.y -= tile_height

                if right_m:
                    if xm + 1 <= level_x and level[ym][xm + 1] != '#':
                        player.rect.x += tile_width
                        xm += 1
                        for i in all_sprites:
                            i.rect.x -= tile_width
                if left_m:
                    if xm - 1 >= 0 and level[ym][xm - 1] != '#':
                        player.rect.x -= tile_width
                        xm -= 1
                        for i in all_sprites:
                            i.rect.x += tile_width

            screen.fill((200, 200, 200))
            all_sprites.draw(screen)
            player_group.draw(screen)
            for sprite in plant_group:
                sprite.time += sprite.clock.tick()
                if sprite.cur_frame < 5 and sprite.time >= sprite.delay:
                    sprite.cur_frame += 1
                    sprite.time = 0
                    sprite.update()
            font = pygame.font.Font(None, 50)
            text = font.render(f'Собрано растений: {player.collected}', True, (100, 255, 100))
            enemy.time += enemy.clock.tick()
            # if enemy.time >= enemy.delay:
            #     enemy.move_towards_player(player)

            screen.blit(text, (20, 0))

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
        self.collected = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.time += self.clock.tick()
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
                # AnimatedSprite(load_image("Sprout Lands - Sprites - Basic pack\Objects\Basic_Plants.png"), 6, 2, x, y)
                new_player = Player(x, y)
                # x0, y0 = x, y
            elif level[y][x] == 'f':
                Tile('empty', x, y)
                Plant(load_image("Sprout Lands - Sprites - Basic pack\Objects\Basic_Plants.png"), 6, 2, x, y)
    # x, y = 200, 150
    # new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

start_screen()
