import pygame
from random import randint


class Player1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group=None):
        super().__init__()
        # self.w = 70
        # self.h = 70
        self.rect = pygame.Rect(pos_x * 25, pos_y * 25, 50, 50)
        self.group = group
        routes = [1, -1, 2, -2]
        self.route = routes[randint(0, 3)]
        self.rect.x = pos_x * 25
        self.rect.y = pos_y * 25
        self.turn = -1
        self.speed = 5
        self.status = 0
        # self.status = True

    def move(self):
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