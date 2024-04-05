import pygame
import sqlite3
import os
from logic.player1 import Player1
from logic.player2 import Player2
from logic.block import Block


def add_to_database(level, score):
    con = sqlite3.connect("results_db.sqlite")
    cur = con.cursor()
    cur.execute(f'INSERT INTO results(level,score) VALUES({level}, {score})')
    con.commit()
    con.close()


def get_from_database():
    con = sqlite3.connect("results_db.sqlite")
    cur = con.cursor()
    data = cur.execute(f'SELECT score FROM results').fetchall()
    max_value = max(map(lambda x: int(*x), data))
    con.close()
    return max_value


def draw_blocks():
    for b in blocks:
        screen.blit(b.color, (b.rect.x, b.rect.y))


def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
    image = pygame.image.load(fullname)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def generate_level(level):
    global map_width, map_height
    global screen_color
    # new_player, x, y = None, None, None
    color = (0, 0, 0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'f':
                color = fence
                blocks.append(Block((x, y), color))
            elif level[y][x] == '.':
                color = field
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'g':
                color = grass
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'i':
                color = ice
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'b':
                color = brick
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'w':
                color = water
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'm':
                color = metal
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'M':
                color = metal_half
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'u':
                color = upper_brick
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'l':
                color = lower_brick
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'L':
                color = left_brick
                blocks.append(Block((x, y), color))
            elif level[y][x] == 'R':
                color = right_brick
                blocks.append(Block((x, y), color))

    map_width = 50 * len(level[0])
    map_height = 50 * len(level)
    # return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def game():
    level_n = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                add_to_database(level_n, score)
                terminate()
        # for i in range(10):
        #     screen.blit(variable with picture, (10 + i * 50, 260)) # отрисовать количество
        #     очков, жизней, тп в углу экрана
        draw_blocks()
        pygame.display.flip()
        clock.tick(FPS)


size = width, height = 1400, 700
WIDTH, HEIGHT = width, height
screen = pygame.display.set_mode(size)
map_width, map_height = 0, 0
# programIcon = pygame.image.load('data/icon.png') # иконка программы
# pygame.display.set_icon(programIcon)
FPS = 50
clock = pygame.time.Clock()
# high_score = get_from_database()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
blocks = []
players = []

field = load_image('field.png')
brick = load_image('brick.png')
lower_brick = load_image('lower_brick.png')
upper_brick = load_image('upper_brick.png')
left_brick = load_image('Left_brick.png')
right_brick = load_image('Right_brick.png')
grass = load_image('grass.png')
water = load_image('water.png')
ice = load_image('ice.png')
fence = load_image('fence.png')
metal = load_image('metal.png')
metal_half = load_image('metal_half.png')
pygame.display.set_caption('Battle City')
map_name = "map.txt"
generate_level(load_level(map_name))

game()
