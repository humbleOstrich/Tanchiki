import pygame
from random import randint


class Player1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color, group):
        super().__init__(group)
        # self.w = 70
        # self.h = 70
        self.rect = pygame.Rect(pos_x * 25, pos_y * 25, 50, 50)
        # self.group = group
        routes = [1, -1, 2, -2]
        self.route = routes[randint(0, 3)]
        self.rect.x = pos_x * 25
        self.rect.y = pos_y * 25
        self.turn = -1
        self.speed = 5
        self.status = 0
        self.color = color
        self.shooting = 0
        self.number = 1
        self.under_grass = False

    def move(self):
        if self.shooting == 0:
            if self.route == 1:
                self.rect = self.rect.move(self.speed, 0)
            elif self.route == -1:
                self.rect = self.rect.move(-self.speed, 0)
            elif self.route == 2:
                self.rect = self.rect.move(0, self.speed)
            elif self.route == -2:
                self.rect = self.rect.move(0, -self.speed)

    # def update(self):
    #     screen.blit(ghost_food, (self.rect.x, self.rect.y))