import pygame
import sqlite3
import os
import sys
from logic.player1 import Player1
from logic.player2 import Player2
from logic.block import Block
from logic.fence import Fence
from random import randint
from copy import copy


# def add_to_database(level, score):
#     con = sqlite3.connect("tanks.sqlite")
#     cur = con.cursor()
#     cur.execute(f'INSERT INTO res(level,score) VALUES({level}, {score})')
#     con.commit()
#     con.close()
#
#
# def get_from_database():
#     con = sqlite3.connect("tanks.sqlite")
#     cur = con.cursor()
#     data = cur.execute(f'SELECT score FROM res').fetchall()
#     max_value = max(map(lambda x: int(*x), data))
#     con.close()
#     return max_value


def draw_blocks():
    # for f in field_blocks:
    #     screen.blit(f.color, (f.rect.x, f.rect.y))
    for b in blocks:
        screen.blit(b.color, (b.rect.x, b.rect.y))
    # screen.blit(order_1, (630, 0))
    # screen.blit(order_2, (770, 630))


def draw_grass():
    for g in grass_blocks:
        screen.blit(g.color, (g.rect.x, g.rect.y))


def draw_tanks():
    for t in tanks1:
        # print(t.rect.x, t.rect.y)
        # screen.blit(tank_img, (t.rect.x, t.rect.y))
        # pygame.draw.rect(screen, (255, 0, 0), (t.rect.x, t.rect.y, 50, 50))
        if t.shooting > 0:
            t.color = tank1_shooting
            t.shooting -= 1
        elif t.shooting < 0:
            t.color = shot
            t.shooting += 1
        screen.blit(t.color, (t.rect.x, t.rect.y))
    for t in tanks2:
        # print(t.rect.x, t.rect.y)
        if t.shooting > 0:
            t.color = tank2_shooting
            t.shooting -= 1
        elif t.shooting < 0:
            t.color = shot
            t.shooting += 1
        screen.blit(t.color, (t.rect.x, t.rect.y))
        # pygame.draw.rect(screen, (255, 0, 0), (t.rect.x, t.rect.y, 50, 50))


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
    # global map_width, map_height
    global screen_color
    # new_player, x, y = None, None, None
    color = (0, 0, 0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 's':
                spawn1.append([x, y])
                blocks.append(Block(x, y, color, True))
            elif level[y][x] == 'z':
                spawn2.append([x, y])
                blocks.append(Block(x, y, color, True))
            elif level[y][x] == '.' or level[y][x] == 'u' or level[y][x] == 'd'\
                    or level[y][x] == 'l' or level[y][x] == 'r':
                color = field
                blocks.append(Block(x, y, color, True))
            elif level[y][x] == 'g':
                blocks.append(Block(x, y, field, True))
                grass_blocks.append(Block(x, y, grass, True))
            elif level[y][x] == 'i':
                color = ice
                blocks.append(Block(x, y, color, True))
            elif level[y][x] == 'b':
                color = brick
                blocks.append(Block(x, y, color, False))
            elif level[y][x] == 'w':
                color = water
                blocks.append(Block(x, y, color, False))
            elif level[y][x] == 'm':
                color = metal
                blocks.append(Block(x, y, color, False))

    # map_width = 50 * len(level[0])
    # map_height = 50 * len(level)
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


def spawn(n):
    a = randint(0, 1)
    if n == 1:
        x, y = spawn1[a]
        entity = Player1(x, y, copy(tank1), tanks1_gr)
        tanks1.append(entity)
        all_tanks.append(entity)
    else:
        x, y = spawn2[a]
        entity = Player2(x, y, copy(tank2), tanks2_gr)
        tanks2.append(entity)
        all_tanks.append(entity)


# def fire_anim():
#     pass


def fire(predator, prey):
    predator.shooting = 100
    prey.shooting = -100


def check_fire():
    for i in tanks1:
        for j in tanks2:
            if i.rect.x in range(j.rect.x - 24, j.rect.x + 24):
                a, b = 0, 0
                top = i if i.rect.y < j.rect.y else j
                bottom = i if i.rect.y > j.rect.y else j
                for p in blocks:
                    if p.type == False and p.rect.y in range(min(i.rect.y, j.rect.y),
                                                             max(i.rect.y, j.rect.y)):
                        break
                else:
                    if top.route == 2:
                        a = 1
                    elif top.route == -1 or top.route == 1:
                        a = 0.5
                    if bottom.route == -2:
                        b = 1
                    elif bottom.route == -1 or bottom.route == 1:
                        b = 0.5
                    if a > b:
                        top.route = 2
                        fire(top, bottom)
                    elif b > a:
                        bottom.route = -2
                        fire(bottom, top)
            if i.rect.y in range(j.rect.y - 24, j.rect.y + 24):
                a, b = 0, 0
                left = i if i.rect.x < j.rect.x else j
                right = i if i.rect.x > j.rect.x else j
                for p in blocks:
                    if p.type == False and p.rect.x in range(min(i.rect.x, j.rect.x),
                                                             max(i.rect.x, j.rect.x)):
                        break
                    else:
                        if left.route == 1:
                            a = 1
                        elif left.route == -2 or left.route == 2:
                            a = 0.5
                        if right.route == -1:
                            b = 1
                        elif right.route == -2 or right.route == 2:
                            b = 0.5
                        if a > b:
                            left.route = 1
                            fire(left, right)
                        else:
                            right.route = -1
                            fire(right, left)


def flip_sprite(s):
    route = s.route
    if s.number == 1:
        if s.route == -2:
            s.color = tank1
        elif s.route == 2:
            s.color = pygame.transform.flip(tank1, False, True)
        elif s.route == -1:
            s.color = pygame.transform.rotate(tank1, 90)
        elif s.route == 1:
            s.color = pygame.transform.rotate(tank1, -90)
    else:
        if s.route == -2:
            s.color = tank2
        elif s.route == 2:
            s.color = pygame.transform.flip(tank2, False, True)
        elif s.route == -1:
            s.color = pygame.transform.rotate(tank2, 90)
        elif s.route == 1:
            s.color = pygame.transform.rotate(tank2, -90)


# def check_collision(t1, t2):
    # if t1.rect.right > t2.rect.left and \
    #         t1.rect.left < t2.rect.right and \
    #         t1.rect.bottom > t2.rect.top and \
    #         t1.rect.top < t2.rect.bottom:
    #     return True
    # if t2.rect.right > t1.rect.left and \
    #         t2.rect.left < t1.rect.right and \
    #         t2.rect.bottom > t1.rect.top and \
    #         t2.rect.top < t1.rect.bottom:
    #     return True
    # return False


def change_route(ent):
    cr = ent.route
    possible_routes = [-1, 1, -2, 2]
    route = possible_routes[randint(0, 3)]
    while route == cr:
        route = possible_routes[randint(0, 3)]
    return route


def col_check(group, n):
    for t1 in group:
        if t1.shooting == -1:
            all_tanks.remove(t1)
            if n == 1:
                tanks1.remove(t1)
                tanks1_gr.remove(t1)
            else:
                tanks2.remove(t1)
                tanks2_gr.remove(t1)
        elif t1.shooting < -1:
            t1.shooting += 1
        elif t1.shooting > 0:
            t1.shooting -= 1
        else:
            if t1.route == 1:
                mob = pygame.Rect(t1.rect.x + speed, t1.rect.y, 50, 50)
            elif t1.route == -1:
                mob = pygame.Rect(t1.rect.x - speed, t1.rect.y, 50, 50)
            elif t1.route == 2:
                mob = pygame.Rect(t1.rect.x, t1.rect.y + speed, 50, 50)
            elif t1.route == -2:
                mob = pygame.Rect(t1.rect.x, t1.rect.y - speed, 50, 50)
            for b in blocks:
                if b.type == False and mob.colliderect(b):
                    t1.route = change_route(t1)
                    flip_sprite(t1)
                    break
                elif b.color == ice and ((mob.x == b.rect.x and mob.y == b.rect.y)
                or (mob.x + 25 == b.rect.x + 25 and mob.y + 25 == b.rect.y + 25)):
                    t1.status = 100
                    t1.speed = 9
            else:
                t1.move()
            t1.status -= 1
            if t1.status <= 0:
                t1.speed = 5


def collision(group):
    for t1 in group:
        if t1.shooting == 0:
            if t1.route == 1:
                mob1 = pygame.Rect(t1.rect.x + speed, t1.rect.y, 50, 50)
            elif t1.route == -1:
                mob1 = pygame.Rect(t1.rect.x - speed, t1.rect.y, 50, 50)
            elif t1.route == 2:
                mob1 = pygame.Rect(t1.rect.x, t1.rect.y + speed, 50, 50)
            elif t1.route == -2:
                mob1 = pygame.Rect(t1.rect.x, t1.rect.y - speed, 50, 50)
            for t2 in group:
                if t1 != t2:
                    if t2.route == 1:
                        mob2 = pygame.Rect(t2.rect.x + speed, t2.rect.y, 50, 50)
                    elif t2.route == -1:
                        mob2 = pygame.Rect(t2.rect.x - speed, t2.rect.y, 50, 50)
                    elif t2.route == 2:
                        mob2 = pygame.Rect(t2.rect.x, t2.rect.y + speed, 50, 50)
                    elif t2.route == -2:
                        mob2 = pygame.Rect(t2.rect.x, t2.rect.y - speed, 50, 50)
                    if mob1.colliderect(mob2):
                        t1.route = -t1.route
                        t2.route = -t2.route
                        flip_sprite(t1)
                        flip_sprite(t2)


def game():
    global tk1, tk2, spawn_delay1, spawn_delay2
    level_n = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # add_to_database(level_n, score)
                terminate()
        # for i in range(10):
        #     screen.blit(variable with picture, (10 + i * 50, 260)) # отрисовать количество
        #     очков, жизней, тп в углу экрана
        if tk1 < 5 and spawn_delay1 <= 0:
            spawn(1)
            tk1 += 1
            spawn_delay1 = 100
        if tk2 < 5 and spawn_delay2 <= 0:
            spawn(2)
            tk2 += 1
            spawn_delay2 = 100
        # for t1 in tanks1:
        #     for t2 in tanks2:
        #         if t1.rect.colliderect(t2.rect):
        #             t1.route = change_route(t1, t1.route)
        #             t2.route = change_route(t2, t2.route)
        # for i in all_tanks:
        #     for j in all_tanks:
        #         if i != j and check_collision(i, j):
        #             print('collision')
        spawn_delay1 -= 1
        spawn_delay2 -= 1
        collision(tanks1)
        collision(tanks2)
        col_check(tanks1)
        col_check(tanks2)
        check_fire()
        # for i in all_tanks:
        #     i.move()
        screen.fill((0, 0, 0))
        draw_blocks()
        draw_tanks()
        # draw_grass()
        pygame.display.flip()
        clock.tick(FPS)


size = width, height = 1400, 700
WIDTH, HEIGHT = width, height
screen = pygame.display.set_mode(size)
# map_width, map_height = 0, 0
# programIcon = pygame.image.load('data/icon.png') # иконка программы
# pygame.display.set_icon(programIcon)
FPS = 50
clock = pygame.time.Clock()
# high_score = get_from_database()

# all_sprites = pygame.sprite.Group()
# player_group = pygame.sprite.Group()
blocks = []
grass_blocks = []
field_blocks = []
# all_sprites = pygame.sprite.Group()
tanks1 = []
tanks2 = []
all_tanks = tanks1[:] + tanks2[:]
spawn1 = []
spawn2 = []
tanks1_gr = pygame.sprite.Group()
tanks2_gr = pygame.sprite.Group()
speed = 5
tk1 = 0
tk2 = 0
spawn_delay1 = 0
spawn_delay2 = 0

field = load_image('field2.png')
brick = load_image('brick2.png')
# lower_brick = load_image('lower_brick.png')
# upper_brick = load_image('upper_brick.png')
# left_brick = load_image('Left_brick.png')
# right_brick = load_image('Right_brick.png')
grass = load_image('grass2.png')
water = load_image('water2.png')
ice = load_image('ice2.png')
# fence = load_image('fence.png')
metal = load_image('metal2.png')
# metal_half = load_image('metal_half.png')
# order_1 = load_image('order_1.png')
# order_2 = load_image('order_2.png')
# ghost = load_image('red2.png')
tank1 = load_image('blue_tank.png')
tank2 = load_image('tank_green.png')
tank1_shooting = load_image('blue_tank_shooting.png')
tank2_shooting = load_image('tank_green_shooting.png')
shot = load_image('shot.png')
pygame.display.set_caption('Battle City')
map_name = "levels/level1.txt"
generate_level(load_level(map_name))

game()