import pygame


class Block(pygame.sprite.Sprite):

    def __init__(self, x, y, color, type):
        super().__init__()
        self.rect = pygame.Rect(x * 25, y * 25, 25, 25)
        self.rect.x = x * 25
        self.rect.y = y * 25
        self.color = color
        self.type = type
