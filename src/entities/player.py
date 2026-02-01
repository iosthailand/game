import pygame
from settings import *
from .base_entity import BaseEntity

class Player(BaseEntity):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y, scene.all_sprites)
        self.load_animations()
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_dir = pygame.math.Vector2(1, 0)
        
        # Animation state (overriding BaseEntity variables for clarity)
        self.frame_index = 0
        self.last_update = 0
        self.is_moving = False
        self.facing_right = True

    def load_animations(self):
        # Load the sheet
        sheet = self.game.resource_manager.load_image('hero', 'hero_run.png')
        self.animations = {'run': [], 'idle': []}
        
        # Frame size is 256x256 in a 1024x1024 sheet (4 frames horizontal)
        for i in range(4):
            rect = pygame.Rect(i * 256, 0, 256, 256)
            frame = pygame.Surface((256, 256), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            # Scale to TILESIZE * 1.5 for better proportions
            size = int(TILESIZE * 1.5)
            scaled_frame = pygame.transform.scale(frame, (size, size))
            self.animations['run'].append(scaled_frame)
        
        self.animations['idle'].append(self.animations['run'][0])

    def animate(self):
        now = pygame.time.get_ticks()
        
        # Select base frame from right-facing list
        if self.vx != 0 or self.vy != 0:
            self.is_moving = True
            if now - self.last_update > 100: # 10fps
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(self.animations['run'])
            
            # Use the currently calculated frame_index
            self.image = self.animations['run'][self.frame_index]
        else:
            self.is_moving = False
            self.frame_index = 0
            self.image = self.animations['idle'][0]

        # Apply flip to the selected base image if needed
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            
        # Update rect maintaining center for consistency
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.last_dir = pygame.math.Vector2(-1, 0)
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.last_dir = pygame.math.Vector2(1, 0)
            self.facing_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
            self.last_dir = pygame.math.Vector2(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = PLAYER_SPEED
            self.last_dir = pygame.math.Vector2(0, 1)
            
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
            self.last_dir = pygame.math.Vector2(self.vx, self.vy).normalize()

    def shoot(self):
        from .bullet import Bullet
        Bullet(self.scene, self.rect.centerx, self.rect.centery, self.last_dir)

    def update(self):
        self.get_keys()
        # animate() is called within super().update()
        super().update()
