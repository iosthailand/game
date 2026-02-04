import pygame
from settings import *

class Decoration(pygame.sprite.Sprite):
    def __init__(self, scene, x, y, image_name, groups, anchor='topleft'):
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        self.game = scene.game
        
        # Load image from resource manager (native size)
        self.image = self.game.resource_manager.load_image(image_name, image_name)
        self.rect = self.image.get_rect()
        
        # Set position based on anchor
        setattr(self.rect, anchor, (x, y))
        
    def update(self):
        # Decorations are static, no logic needed
        pass
