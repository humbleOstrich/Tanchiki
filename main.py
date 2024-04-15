import pygame
import sqlite3
import os
import sys
from logic.player1 import Player1
from logic.player2 import Player2
from logic.block import Block
from random import randint
from copy import copy


def draw_blocks():
    for b in blocks:
        screen.blit(b.color, (b.rect.x, b.rect.y))


def draw_grass():
    for g in grass_blocks:
        screen.blit(g.color, (g.rect.x, g.rect.y))


def draw_tanks():
    for t in dead_tanks:
        screen.blit(t.color, (t.rect.x, t.rect.y))
    for t in tanks1:
        if t.shooting >= 0:
            screen.blit(t.color, (t.rect.x, t.rect.y))
    for t in tanks2:
        if t.shooting >= 0:
            screen.blit(t.color, (t.rect.x, t.rect.y))


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
    global screen_color
    color = (0, 0, 0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 's':
                spawn1.append([x, y])
                blocks.append(Block(x, y, field, True))
            elif level[y][x] == 'z':
                spawn2.append([x, y])
                blocks.append(Block(x, y, field, True))
            elif level[y][x] == '.' or level[y][x] == 'u' or level[y][x] == 'd'\
                    or level[y][x] == 'l' or level[y][x] == 'r':
                blocks.append(Block(x, y, field, True))
            elif level[y][x] == 'g':
                blocks.append(Block(x, y, field, True))
                grass_blocks.append(Block(x, y, grass, True))
            elif level[y][x] == 'i':
                blocks.append(Block(x, y, ice, True))
            elif level[y][x] == 'b':
                blocks.append(Block(x, y, field, True))
                blocks.append(Block(x, y, brick, False))
            elif level[y][x] == 'w':
                blocks.append(Block(x, y, water, False))
            elif level[y][x] == 'm':
                blocks.append(Block(x, y, metal, False))


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
    global tk1, tk2, spawn_delay1, spawn_delay2
    a = randint(0, 1)
    # print('spawn', n, tk1, tk2)
    if n == 1:
        x, y = spawn1[a]
        for i in all_tanks:
            if i.rect.x in range(x - 100, x + 50) or i.rect.y in range(y - 100, y + 50):
                break
        else:
            entity = Player1(x, y, copy(tank1), tanks1_gr)
            tanks1.append(entity)
            flip_sprite(entity, True)
            all_tanks.append(entity)
            tk1 += 1
            spawn_delay1 = 100
    else:
        x, y = spawn2[a]
        for i in all_tanks:
            if i.rect.x in range(x - 100, x + 50) or i.rect.y in range(y - 100, y + 50):
                break
        else:
            entity = Player2(x, y, copy(tank2), tanks2_gr)
            tanks2.append(entity)
            flip_sprite(entity, True)
            all_tanks.append(entity)
            tk2 += 1
            spawn_delay2 = 100


def fire(predator, prey, flag=True):
    # print(dead_tanks)
    if not flag:
        predator.shooting = -50
        prey.shooting = -50
        predator.color = shot
        prey.color = shot
        dead_tanks.append(predator)
        dead_tanks.append(prey)
    else:
        predator.shooting = 80
        prey.shooting = -50
        dead_tanks.append(prey)
        if predator.number == 1:
            predator.color = tank1_shooting
        else:
            predator.color = tank2_shooting
        prey.color = shot
        flip_sprite(predator, False)


def check_fire():
    for i in tanks1:
        if i.shooting == 0:
            for j in tanks2:
                if j.shooting == 0:
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
                            elif a == b == 1:
                                fire(top, bottom, False)
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
                            elif b > a:
                                right.route = -1
                                fire(right, left)
                            elif a == b == 1:
                                fire(right, left, False)


def flip_sprite(s, flag):
    route = s.route
    if flag:
        if s.number == 1:
            t = tank1
        else:
            t = tank2
    else:
        if s.number == 1:
            t = tank1_shooting
        else:
            t = tank2_shooting
    if s.route == -2:
        s.color = t
    elif s.route == 2:
        s.color = pygame.transform.flip(t, False, True)
    elif s.route == -1:
        s.color = pygame.transform.rotate(t, 90)
    elif s.route == 1:
        s.color = pygame.transform.rotate(t, -90)


def change_route(ent):
    cr = ent.route
    possible_routes = [-1, 1, -2, 2]
    route = possible_routes[randint(0, 3)]
    while route == cr:
        route = possible_routes[randint(0, 3)]
    return route


def fire_brick(t, b):
    t.shooting = 35
    if t.number == 1:
        t.color = tank1_shooting
    else:
        t.color = tank2_shooting
    flip_sprite(t, False)
    blocks.remove(b)


def col_check(group, n, enemy):
    for t1 in group:
        if t1.shooting == -1:
            all_tanks.remove(t1)
            dead_tanks.remove(t1)
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
            if t1.shooting == 0:
                if n == 1:
                    t1.color = tank1
                else:
                    t1.color = tank2
                flip_sprite(t1, True)
        else:
            if t1.route == 1:
                mob = pygame.Rect(t1.rect.x + t1.speed, t1.rect.y, 50, 50)
            elif t1.route == -1:
                mob = pygame.Rect(t1.rect.x - t1.speed, t1.rect.y, 50, 50)
            elif t1.route == 2:
                mob = pygame.Rect(t1.rect.x, t1.rect.y + t1.speed, 50, 50)
            elif t1.route == -2:
                mob = pygame.Rect(t1.rect.x, t1.rect.y - t1.speed, 50, 50)
            for t2 in enemy:
                en = pygame.Rect(t2.rect.x, t2.rect.y, 50, 50)
                if mob.colliderect(en) and t2.shooting > 0:
                    t1.route = change_route(t1)
                    flip_sprite(t1, True)
                    break
            for b in blocks:
                if b.type == False and mob.colliderect(b):
                    if b.color == brick:
                        fire_chance = randint(0, 2)
                        if fire_chance == 1:
                            fire_brick(t1, b)
                            break
                        else:
                            t1.route = change_route(t1)
                            flip_sprite(t1, True)
                            break
                    else:
                        t1.route = change_route(t1)
                        flip_sprite(t1, True)
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
                mob1 = pygame.Rect(t1.rect.x + t1.speed, t1.rect.y, 50, 50)
            elif t1.route == -1:
                mob1 = pygame.Rect(t1.rect.x - t1.speed, t1.rect.y, 50, 50)
            elif t1.route == 2:
                mob1 = pygame.Rect(t1.rect.x, t1.rect.y + t1.speed, 50, 50)
            elif t1.route == -2:
                mob1 = pygame.Rect(t1.rect.x, t1.rect.y - t1.speed, 50, 50)
            for t2 in group:
                if t1 != t2 and t2.shooting >= 0:
                    if t2.route == 1:
                        mob2 = pygame.Rect(t2.rect.x + t2.speed, t2.rect.y, 50, 50)
                    elif t2.route == -1:
                        mob2 = pygame.Rect(t2.rect.x - t2.speed, t2.rect.y, 50, 50)
                    elif t2.route == 2:
                        mob2 = pygame.Rect(t2.rect.x, t2.rect.y + t2.speed, 50, 50)
                    elif t2.route == -2:
                        mob2 = pygame.Rect(t2.rect.x, t2.rect.y - t2.speed, 50, 50)
                    if mob1.colliderect(mob2):
                        t1.route = -t1.route
                        flip_sprite(t1, True)
                        # if t2.shooting == 0:
                        t2.route = -t2.route
                        flip_sprite(t2, True)


def game():
    global tk1, tk2, spawn_delay1, spawn_delay2
    level_n = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if tk1 < 5 and spawn_delay1 <= 0:
            spawn(1)
            # tk1 += 1
            # spawn_delay1 = 100
        if tk2 < 5 and spawn_delay2 <= 0:
            spawn(2)
            # tk2 += 1
            # spawn_delay2 = 100
        spawn_delay1 -= 1
        spawn_delay2 -= 1
        collision(tanks1)
        collision(tanks2)
        col_check(tanks1, 1, tanks2)
        col_check(tanks2, 2, tanks1)
        check_fire()
        screen.fill((0, 0, 0))
        draw_blocks()
        draw_tanks()
        draw_grass()
        pygame.display.flip()
        clock.tick(FPS)


size = width, height = 1400, 700
WIDTH, HEIGHT = width, height
screen = pygame.display.set_mode(size)
# programIcon = pygame.image.load('data/icon.png')
# pygame.display.set_icon(programIcon)
FPS = 50
clock = pygame.time.Clock()

blocks = []
grass_blocks = []
field_blocks = []

tanks1 = []
tanks2 = []
dead_tanks = []
all_tanks = tanks1[:] + tanks2[:]
spawn1 = []
spawn2 = []
tanks1_gr = pygame.sprite.Group()
tanks2_gr = pygame.sprite.Group()

tk1 = 0
tk2 = 0
spawn_delay1 = 0
spawn_delay2 = 0

field = load_image('field2.png')
brick = load_image('brick2.png')
grass = load_image('grass2.png')
water = load_image('water2.png')
ice = load_image('ice2.png')
metal = load_image('metal2.png')
tank1 = load_image('blue_tank.png')
tank2 = load_image('green_tank.png')
tank1_shooting = load_image('blue_tank_shooting.png')
tank2_shooting = load_image('green_tank_shooting.png')
shot = load_image('shot.png')
pygame.display.set_caption('Battle City')
map_name = "levels/level1.txt"
generate_level(load_level(map_name))

game()
