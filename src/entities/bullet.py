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

class EnemyBullet(Bullet):
    def __init__(self, scene, x, y, direction):
        super().__init__(scene, x, y, direction)
        # Change groups so it doesn't hit enemies
        self.remove(scene.bullets)
        scene.enemy_bullets.add(self)
        self.image.fill(RED) # Hostile bullets are red
        self.speed = 300 # Hostile bullets are a bit slower

class WizardBullet(Bullet):
    def __init__(self, scene, x, y, direction):
        super().__init__(scene, x, y, direction)
        # Change groups so it doesn't hit enemies
        self.remove(scene.bullets)
        scene.enemy_bullets.add(self)
        self.image.fill((138, 43, 226))  # Purple magic bullet
        self.speed = 450  # Faster than normal enemy bullets

