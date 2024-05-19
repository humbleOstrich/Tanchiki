import pygame
import os
import sys
from logic.player1 import Player1
from logic.player2 import Player2
from logic.block import Block
from logic.button import Button
from logic.line import Line
from random import randint
from copy import copy
pygame.init()
pygame.font.init()


font1 = pygame.font.Font(None, 50)
font2 = pygame.font.SysFont("centuryschoolbookполужирный", 150)


def draw_str(line, font=font1):
    return font.render(str(line), True, (219, 215, 210))


def draw_lines():
    for i in lines:
        pygame.draw.line(screen, (255, 0, 0), [i.start_x, i.start_y], [i.end_x, i.end_y], 5)


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


def spawn(n, power=False):
    global spawn_delay1, spawn_delay2, tk1, tk2, tk1_strong, tk2_strong
    a = randint(0, 1)
    if n == 1:
        x, y = spawn1[a]
        for i in all_tanks:
            if i.rect.x in range(x - 100, x + 50) or i.rect.y in range(y - 100, y + 50):
                break
        else:
            if power:
                entity = Player1(x, y, copy(tank1_strong), tanks1_gr, True)
                tk1_strong -= 1
            else:
                entity = Player1(x, y, copy(tank1), tanks1_gr, False)
                tk1 -= 1
            entity.recharge_f()
            tanks1.append(entity)
            flip_sprite(entity, True)
            all_tanks.append(entity)
            spawn_delay1 = 100
    else:
        x, y = spawn2[a]
        for i in all_tanks:
            if i.rect.x in range(x - 100, x + 50) or i.rect.y in range(y - 100, y + 50):
                break
        else:
            if power:
                entity = Player2(x, y, copy(tank2_strong), tanks2_gr, True)
                tk2_strong -= 1
            else:
                entity = Player2(x, y, copy(tank2), tanks2_gr, False)
                tk2 -= 1
            entity.recharge_f()
            tanks2.append(entity)
            flip_sprite(entity, True)
            all_tanks.append(entity)
            spawn_delay2 = 100


def remove_life(entity):
    global s1, s2
    if entity.number == 1:
        s1 -= 1
    else:
        s2 -= 1
    # print(entity.number, "life removed!")


def fire(predator, prey, flag=True):
    # print(dead_tanks)
    if not flag:
        if not predator.power or predator.lives <= 1:
            predator.shooting = -80
            predator.color = shot
            dead_tanks.append(predator)
        else:
            predator.lives -= 1
            predator.shooting = 80
            predator.route = -predator.route
        if not prey.power or prey.lives <= 1:
            prey.shooting = -80
            prey.color = shot
            dead_tanks.append(prey)
        else:
            prey.lives -= 1
            prey.shooting = 80
            prey.route = -prey.route
        remove_life(predator)
        remove_life(prey)
    else:
        predator.bullets -= 1
        predator.shooting = 80
        if not prey.power or prey.lives <= 1:
            prey.shooting = -80
            prey.color = shot
            dead_tanks.append(prey)
        else:
            prey.lives -= 1
            prey.shooting = 80
        # if predator.number == 1:
        #     if predator.power:
        #         predator.color = tank1_strong_shooting
        #     else:
        #         predator.color = tank1_shooting
        # else:
        #     if predator.power:
        #         predator.color = tank2_strong_shooting
        #     else:
        #         predator.color = tank2_shooting
        remove_life(prey)
        flip_sprite(predator, False)
    x, y = predator.rect.x + 25, predator.rect.y + 25
    x1, y1 = prey.rect.x + 25, prey.rect.y + 25
    lines.append(Line(x, y, x1, y1))


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
                            if top.recharge <= 0:
                                a = -100
                            if bottom.recharge <= 0:
                                b = -100
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
                            if left.recharge <= 0:
                                a = -100
                            if right.recharge <= 0:
                                b = -100
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
            if s.power:
                t = tank1_strong
            else:
                t = tank1
        else:
            if s.power:
                t = tank2_strong
            else:
                t = tank2
    else:
        if s.number == 1:
            if s.power:
                t = tank1_strong_shooting
            else:
                t = tank1_shooting
        else:
            if s.power:
                t = tank2_strong_shooting
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
    if t.recharge > 0:
        t.shooting = 35
        t.bullets -= 1
        if t.number == 1:
            if t.power:
                t.color = tank1_strong_shooting
            else:
                t.color = tank1_shooting
        else:
            if t.power:
                t.color = tank2_strong_shooting
            else:
                t.color = tank2_shooting
        flip_sprite(t, False)
        blocks.remove(b)


def col_check(group, n, enemy):
    for t1 in group:
        if t1.bullets <= 0:
            t1.recharge = -300
            t1.recharge_f()
        if t1.shooting == -1:
            print("entered spot")
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
                        if fire_chance == 1 or (t1.power and t1.recharge):
                            fire_brick(t1, b)
                            break
                        else:
                            t1.route = change_route(t1)
                            flip_sprite(t1, True)
                            break
                    elif b.color == water and t1.power:
                        continue
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
            t1.recharge += 1
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


def draw_lives(n):
    global s1, s2
    screen.blit(draw_str("Lives left:"), (10, 30))
    if n == 1:
        img = tank1
        f = 200
        q = s1
    else:
        img = tank2
        f = 0
        q = s2
    for i in range(min(q, 4)):
        screen.blit(img, ((i % 4) * 50, f + 100))
    for i in range(max(0, q - 4)):
        screen.blit(img, ((i % 4) * 50, f + 200))
        # print(25 + (i % 4) * 25, 50 + i // 3 * 50)


def end_screen(n):
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return start_screen()
        if n == 0:
            text1 = draw_str("Draw!", font=font2)
        elif n == 1:
            text1 = draw_str("Player 1 won!", font=font2)
        elif n == 2:
            text1 = draw_str("Player 2 won!", font=font2)
        text2 = draw_str("Press space bar to restart")
        text2_rect = text2.get_rect(center=(width / 2, 450))
        text1_rect = text1.get_rect(center=(width / 2, 250))
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        pygame.display.flip()
        pygame.time.delay(FPS)


def start_screen():
    global tk1, tk2, tk1_strong, tk2_strong, s1, s2
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(screensaver, (0,0))
        two_two = Button(250, 400, button)
        one_three = Button(500, 400, button)
        all_four = Button(750, 400, button)
        if two_two.draw(screen):
            tk1, tk2, tk1_strong, tk2_strong = 2, 2, 2, 2
            s1, s2 = 8, 8
            generate_level(load_level(map_name))
            return game()
        if one_three.draw(screen):
            tk1, tk2, tk1_strong, tk2_strong = 3, 3, 1, 1
            s1, s2 = 6, 6
            generate_level(load_level(map_name))
            return game()
        if all_four.draw(screen):
            tk1, tk2, tk1_strong, tk2_strong = 4, 4, 0, 0
            s1, s2 = 4, 4
            generate_level(load_level(map_name))
            return game()
        pygame.display.flip()
        pygame.time.delay(FPS)


def null_f(n):
    global s1, s2, blocks, grass_blocks, field_blocks, \
        tanks1, tanks2, dead_tanks, all_tanks, spawn1, spawn2, tanks1_gr, \
        tanks2_gr, tk1, tk2, spawn_delay1, spawn_delay2, tk1_strong, tk2_strong, lines
    s1 = 0
    s2 = 0
    lines = []
    blocks = []
    grass_blocks = []
    field_blocks = []
    tanks1 = []
    tanks2 = []
    dead_tanks = []
    all_tanks = tanks1[:] + tanks2[:]
    spawn1 = []
    spawn2 = []
    for i in tanks1_gr:
        i.kill()
    for i in tanks2_gr:
        i.kill()
    tk1 = 0
    tk2 = 0
    tk1_strong = 0
    tk2_strong = 0
    spawn_delay1 = 0
    spawn_delay2 = 0
    return end_screen(n)


def game():
    global tk1, tk2, tk1_strong, tk2_strong, spawn_delay1, spawn_delay2
    level_n = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        # for i in range(10):
        #     screen.blit(variable with picture, (10 + i * 50, 260)) # draw lives
        if ((tk1 + tk1_strong) > 0) and spawn_delay1 <= 0:
            if tk1 > 0:
                spawn(1, power=False)
            elif tk1_strong > 0:
                spawn(1, power=True)
            # tk1 += 1
            # spawn_delay1 = 100
        if ((tk2 + tk2_strong) > 0) and spawn_delay2 <= 0:
            if tk2 > 0:
                spawn(2, power=False)
            elif tk2_strong > 0:
                spawn(2, power=True)
            # tk2 += 1
            # spawn_delay2 = 100

        spawn_delay1 -= 1
        spawn_delay2 -= 1
        collision(tanks1)
        collision(tanks2)
        col_check(tanks1, 1, tanks2)
        col_check(tanks2, 2, tanks1)
        check_fire()
        # for i in all_tanks:
        #     i.move()
        screen.fill((0, 0, 0))
        draw_blocks()
        # s1 = sum(i.lives if i.power else 1 for i in tanks1)
        # s2 = sum(i.lives if i.power else 1 for i in tanks2)
        # print(s1, s2)
        draw_lives(1)
        draw_lives(2)
        draw_tanks()
        draw_grass()
        draw_lines()
        to_remove = []
        for i in lines:
            i.shooting -= 1
            if i.shooting <= 0:
                to_remove.append(i)
        for i in to_remove:
            lines.remove(i)
        if s1 == 0 and s2 > 0:
            return null_f(2)
        elif s2 == 0 and s1 > 0:
            return null_f(1)
        elif s1 == s2 == 0:
            return null_f(0)
        for i in dead_tanks:
            print(i, "i.shooting:", i.shooting)
        pygame.display.flip()
        clock.tick(FPS)


size = width, height = 1400, 700
WIDTH, HEIGHT = width, height
screen = pygame.display.set_mode(size)
programIcon = load_image('icon.png')
pygame.display.set_icon(programIcon)
FPS = 50
clock = pygame.time.Clock()
s1 = 0
s2 = 0

lines = []
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
tk1_strong = 0
tk2_strong = 0
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
tank1_strong = load_image('tank1_strong.png')
tank2_strong = load_image('tank2_strong.png')
tank1_strong_shooting = load_image('tank1_strong.png')
tank2_strong_shooting = load_image('tank2_strong.png')
tank1_shooting = load_image('blue_tank_shooting.png')
tank2_shooting = load_image('green_tank_shooting.png')
shot = load_image('shot.png')
button = load_image('start.png')
screensaver = load_image('screensaver.png')
pygame.display.set_caption('Battle City')
map_name = "levels/level1.txt"

start_screen()
