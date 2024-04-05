import pygame


class Player1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super().__init__()
        self.w = 50
        self.h = 50
        self.rect = pygame.Rect(pos_x * 25, pos_y * 25, self.w, self.h)
        self.group = group
        routes = [1, -1, 2, -2]
        self.route = routes[random.randint(0, 3)]
        self.rect.x = pos_x * 25
        self.rect.y = pos_y * 25
        self.turn = -1
        self.status = True

    def move(self, direction, distance):
        if direction == 1:
            self.rect = self.rect.move(distance, 0)
        elif direction == -1:
            self.rect = self.rect.move(distance, 0)
        elif direction == 2:
            self.rect = self.rect.move(0, distance)
        elif direction == -2:
            self.rect = self.rect.move(0, distance)

    def update(self):
        screen.blit(ghost_food, (self.rect.x, self.rect.y))