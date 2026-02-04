import pygame
from settings import *

class Decoration(pygame.sprite.Sprite):
    def __init__(self, scene, x, y, image_name, groups):
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        self.game = scene.game
        
        # Load image from resource manager
        self.image = self.game.resource_manager.load_image(image_name, image_name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        # Decorations are static, no logic needed
        pass
