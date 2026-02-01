import pygame
import random
from settings import *
from .base_entity import BaseEntity
from .bullet import EnemyBullet, WizardBullet

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
class GoblinArcher(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.speed = PLAYER_SPEED / 6
        self.detect_range = 350
        self.fire_rate = 2000
        self.last_shot = 0
        self.load_animations()
        
    def load_animations(self):
        # Use slime sheet as base for goblin archer (green tinted)
        sheet = self.game.resource_manager.load_image('slime', 'enemy_slime.png')
        self.animations = {'run': [], 'idle': []}
        for i in range(4):
            rect = pygame.Rect(i * 256, 0, 256, 256)
            frame = pygame.Surface((256, 256), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            # Tint green for goblin feel
            frame.fill((100, 255, 100, 255), special_flags=pygame.BLEND_RGBA_MULT)
            scaled_frame = pygame.transform.scale(frame, (TILESIZE, TILESIZE))
            self.animations['run'].append(scaled_frame)
        self.animations['idle'] = [self.animations['run'][0]]
        self.image = self.animations['idle'][0]

    def update(self):
        now = pygame.time.get_ticks()
        player = self.scene.game.player
        
        # Calculate distance to player
        dist = pygame.math.Vector2(player.rect.center).distance_to(self.rect.center)
        
        if dist < self.detect_range:
            # In shooting range - stop and shoot
            self.vx, self.vy = 0, 0
            if now - self.last_shot > self.fire_rate:
                self.last_shot = now
                self.shoot_at_player()
            
            # Only animate and apply BaseEntity physics, skip Enemy's random movement
            self.animate()
            # Call BaseEntity.update directly to skip Enemy's movement logic
            from .base_entity import BaseEntity
            BaseEntity.update(self)
        else:
            # Out of range - use normal Enemy behavior (random movement)
            super().update()

    def animate(self):
        player = self.scene.game.player
        if self.vx == 0:
            # Face player when shooting even if stationary
            now = pygame.time.get_ticks()
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animations['run'])
            
            self.image = self.animations['run'][self.current_frame]
            if player.rect.centerx < self.rect.centerx:
                self.image = pygame.transform.flip(self.image, True, False)
            
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
        else:
            super().animate()

    def shoot_at_player(self):
        player = self.scene.game.player
        dir_vec = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        if dir_vec.length() > 0:
            dir_vec = dir_vec.normalize()
            EnemyBullet(self.scene, self.rect.centerx, self.rect.centery, dir_vec)

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
class Wizard(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.speed = PLAYER_SPEED / 8
        self.detect_range = 500
        self.fire_rate = 3000
        self.last_shot = 0
        self.load_animations()
        
    def load_animations(self):
        # Purple/blue tinted slime for wizard
        sheet = self.game.resource_manager.load_image('slime', 'enemy_slime.png')
        self.animations = {'run': [], 'idle': []}
        for i in range(4):
            rect = pygame.Rect(i * 256, 0, 256, 256)
            frame = pygame.Surface((256, 256), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            # Purple tint for wizard
            frame.fill((180, 100, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
            scaled_frame = pygame.transform.scale(frame, (TILESIZE, TILESIZE))
            self.animations['run'].append(scaled_frame)
        self.animations['idle'] = [self.animations['run'][0]]
        self.image = self.animations['idle'][0]

    def update(self):
        now = pygame.time.get_ticks()
        player = self.scene.game.player
        
        # Calculate distance to player
        dist = pygame.math.Vector2(player.rect.center).distance_to(self.rect.center)
        
        if dist < self.detect_range:
            # In shooting range - stop and shoot
            self.vx, self.vy = 0, 0
            if now - self.last_shot > self.fire_rate:
                self.last_shot = now
                self.shoot_at_player()
            
            # Only animate and apply BaseEntity physics, skip Enemy's random movement
            self.animate()
            # Call BaseEntity.update directly to skip Enemy's movement logic
            from .base_entity import BaseEntity
            BaseEntity.update(self)
        else:
            # Out of range - use normal Enemy behavior (random movement)
            super().update()

    def animate(self):
        player = self.scene.game.player
        if self.vx == 0:
            # Face player when shooting even if stationary
            now = pygame.time.get_ticks()
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animations['run'])
            
            self.image = self.animations['run'][self.current_frame]
            if player.rect.centerx < self.rect.centerx:
                self.image = pygame.transform.flip(self.image, True, False)
            
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
        else:
            super().animate()

    def shoot_at_player(self):
        player = self.scene.game.player
        dir_vec = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        if dir_vec.length() > 0:
            dir_vec = dir_vec.normalize()
            WizardBullet(self.scene, self.rect.centerx, self.rect.centery, dir_vec)
