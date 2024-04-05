import pygame


class Block(pygame.sprite.Sprite):

    def __init__(self, coords, color):
        super().__init__()
        self.rect = pygame.Rect(coords[0] * 70, coords[1] * 70, 70, 70)
        self.rect.x = coords[0] * 70
        self.rect.y = coords[1] * 70
        self.color = color

    # def update(self):
    #     pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, 25, 25))
