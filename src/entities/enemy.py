import pygame
import random
from settings import *
from .base_entity import BaseEntity

class Enemy(BaseEntity):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y, scene.all_sprites)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0
        self.change_dir_time = random.randint(1000, 3000)
        self.speed = PLAYER_SPEED / 2
        
        # Animation state
        self.current_frame = 0
        self.last_update = 0
        self.animations = {'idle': [self.image]}

    def animate(self):
        if hasattr(self, 'animations') and 'idle' in self.animations:
            now = pygame.time.get_ticks()
            if now - self.last_update > 150: # 6.6fps
                self.last_update = now
                anim_list = self.animations.get('run', self.animations['idle'])
                self.current_frame = (self.current_frame + 1) % len(anim_list)
                self.image = anim_list[self.current_frame]
                
                # Flip logic if moving
                if self.vx < 0:
                    self.image = pygame.transform.flip(self.image, True, False)
                
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

    def change_direction(self):
        self.vx = random.choice([-1, 0, 1]) * self.speed
        self.vy = random.choice([-1, 0, 1]) * self.speed
        self.timer = 0
        self.change_dir_time = random.randint(1000, 3000)

    def update(self):
        self.timer += self.game.clock.get_time()
        if self.timer > self.change_dir_time:
            self.change_direction()
            
        old_vx, old_vy = self.vx, self.vy
        self.animate()
        super().update()
        
        # If we hit a wall (vx or vy became 0 in super().update()), change direction immediately
        if (old_vx != 0 and self.vx == 0) or (old_vy != 0 and self.vy == 0):
            self.change_direction()
        
        # Check for encounter with player
        if self.game.player and self.rect.colliderect(self.game.player.rect):
             pass

class Slime(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.speed = PLAYER_SPEED / 4
        self.hp = 1
        self.load_animations()

    def load_animations(self):
        sheet = self.game.resource_manager.load_image('slime', 'enemy_slime.png')
        self.animations = {'run': [], 'idle': []}
        for i in range(4):
            rect = pygame.Rect(i * 256, 0, 256, 256)
            frame = pygame.Surface((256, 256), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            scaled_frame = pygame.transform.scale(frame, (TILESIZE, TILESIZE))
            self.animations['run'].append(scaled_frame)
        self.animations['idle'] = self.animations['run']
        self.image = self.animations['idle'][0]

class Ghost(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.speed = PLAYER_SPEED / 2
        self.load_animations()
        
    def load_animations(self):
        sheet = self.game.resource_manager.load_image('ghost', 'enemy_ghost.png')
        self.animations = {'run': [], 'idle': []}
        for i in range(4):
            rect = pygame.Rect(i * 256, 0, 256, 256)
            frame = pygame.Surface((256, 256), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            # Use original size for better spooky look or scale down
            scaled_frame = pygame.transform.scale(frame, (TILESIZE, TILESIZE))
            self.animations['run'].append(scaled_frame)
        self.animations['idle'] = self.animations['run']
        self.image = self.animations['idle'][0]

    def collide_with_walls(self, dir):
        pass

    def update(self):
        super().update()
        margin = TILESIZE
        hit = False
        if self.rect.left < margin:
            self.x = margin
            self.vx *= -1
            hit = True
        elif self.rect.right > self.scene.map.width - margin:
            self.x = self.scene.map.width - margin - self.rect.width
            self.vx *= -1
            hit = True
            
        if self.rect.top < margin:
            self.y = margin
            self.vy *= -1
            hit = True
        elif self.rect.bottom > self.scene.map.height - margin:
            self.y = self.scene.map.height - margin - self.rect.height
            self.vy *= -1
            hit = True
            
        if hit:
            self.rect.x = self.x
            self.rect.y = self.y
            self.change_direction()

class FastEnemy(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.speed = PLAYER_SPEED * 0.8
        self.change_dir_time = random.randint(500, 1500)
        self.load_animations()

    def load_animations(self):
        # Fallback to red-tinted slime for FastEnemy due to image generation limits
        sheet = self.game.resource_manager.load_image('slime', 'enemy_slime.png').copy()
        sheet.fill((255, 120, 120), special_flags=pygame.BLEND_RGB_MULT)
        
        self.animations = {'run': [], 'idle': []}
        for i in range(4):
            rect = pygame.Rect(i * 256, 0, 256, 256)
            frame = pygame.Surface((256, 256), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            scaled_frame = pygame.transform.scale(frame, (TILESIZE, TILESIZE))
            self.animations['run'].append(scaled_frame)
        self.animations['idle'] = self.animations['run']
        self.image = self.animations['idle'][0]
