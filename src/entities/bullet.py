import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, scene, x, y, direction):
        self.groups = scene.all_sprites, scene.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        self.game = scene.game
        self.image = pygame.Surface((8, 8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)
        self.speed = 500
        self.direction = direction # Vector2

    def update(self):
        self.x += self.direction.x * self.speed * self.game.dt
        self.y += self.direction.y * self.speed * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Check collision with walls
        if pygame.sprite.spritecollide(self, self.scene.walls, False):
            self.kill()
            
        # Check if out of bounds (map bounds)
        if self.x < 0 or self.x > self.scene.map.width or \
           self.y < 0 or self.y > self.scene.map.height:
            self.kill()
