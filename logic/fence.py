import pygame


class Fence(pygame.sprite.Sprite):

    def __init__(self, stepx, stepy, color):
        super().__init__()
        self.rect = pygame.Rect(stepx, stepy, 35, 70)
        self.rect.x = stepx
        self.rect.y = stepy
        self.color = color