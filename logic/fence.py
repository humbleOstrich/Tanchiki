import pygame


class Fence(pygame.sprite.Sprite):

    def __init__(self, coords, color):
        super().__init__()
        self.rect = pygame.Rect(coords[0] * 70, coords[1] * 70, 70, 70)
        self.rect.x = coords[0] * 70
        self.rect.y = coords[1] * 70
        self.color = color