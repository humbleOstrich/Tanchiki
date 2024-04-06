import pygame


class Block(pygame.sprite.Sprite):

    def __init__(self, stepx, stepy, color):
        super().__init__()
        self.rect = pygame.Rect(stepx, stepy, 70, 70)
        self.rect.x = stepx
        self.rect.y = stepy
        self.color = color

    # def update(self):
    #     pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, 25, 25))
