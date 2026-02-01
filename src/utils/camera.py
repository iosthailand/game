import pygame
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size or center if smaller than screen
        if self.width < WIDTH:
            x = (WIDTH - self.width) // 2
        else:
            x = min(0, x)  # left
            x = max(-(self.width - WIDTH), x)  # right

        if self.height < HEIGHT:
            y = (HEIGHT - self.height) // 2
        else:
            y = min(0, y)  # top
            y = max(-(self.height - HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
