import pygame
from settings import *

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, scene, x, y, groups):
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        self.game = scene.game
        self.x = x
        self.y = y
        self.vx, self.vy = 0, 0
        
        # Animation
        self.animations = {}
        self.current_anim = None
        self.frame_index = 0
        self.last_update = 0
        self.anim_speed = 150 # ms per frame
        
        # Health
        self.max_health = 100
        self.health = self.max_health

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.scene.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.scene.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def animate(self):
        now = pygame.time.get_ticks()
        if self.current_anim and self.current_anim in self.animations:
            if now - self.last_update > self.anim_speed:
                self.last_update = now
                frames = self.animations[self.current_anim]
                self.frame_index = (self.frame_index + 1) % len(frames)
                self.image = frames[self.frame_index]

    def update(self):
        # Base movement logic
        self.x += self.vx * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        # Clamp X to world bounds
        if self.rect.left < 0:
            self.x = 0
            self.rect.left = 0
        elif self.rect.right > self.scene.map.width:
            self.x = self.scene.map.width - self.rect.width
            self.rect.right = self.scene.map.width

        self.y += self.vy * self.game.dt
        self.rect.y = self.y
        self.collide_with_walls('y')
        # Clamp Y to world bounds
        if self.rect.top < 0:
            self.y = 0
            self.rect.top = 0
        elif self.rect.bottom > self.scene.map.height:
            self.y = self.scene.map.height - self.rect.height
            self.rect.bottom = self.scene.map.height

        self.animate()
