import pygame
import os
import random
from settings import *
from .base_scene import BaseScene
from ..utils.map_loader import Map, Tile
from ..utils.camera import Camera
from ..entities.player import Player
from ..entities.enemy import Enemy, Slime, Ghost, FastEnemy

class WorldScene(BaseScene):
    def __init__(self, manager, level_id=1):
        super().__init__(manager)
        self.level_id = level_id
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group() # New group for hostile projectiles
        self.encounter_timer = 1500 # 1.5s grace period when level starts
        self.transitioning = False
        self.load_level_config()
        self.load_world()

    def load_level_config(self):
        import json
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'levels.json')
        with open(config_path, 'r') as f:
            data = json.load(f)
            self.level_config = next((level for level in data['levels'] if level['id'] == self.level_id), data['levels'][0])

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Attack
                    self.game.player.shoot()

    def load_world(self):
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', self.level_config['map_file'])
        
        self.map = Map(data_path)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.game.spawn_manager.spawn_tile(self, col, row)
                if tile == 'P':
                    self.game.spawn_manager.spawn_player(self, col * TILESIZE, row * TILESIZE)
        
        # Spawn enemies based on config
        self.game.spawn_manager.spawn_enemies(self, self.map.data, self.level_config)
                    
        self.camera = Camera(self.map.width, self.map.height)
        if hasattr(self.game, 'player'):
            self.camera.update(self.game.player)

    def update(self, dt):
        self.all_sprites.update()
        self.camera.update(self.game.player)
        
        # Encounter cooldown
        if self.encounter_timer > 0:
            self.encounter_timer -= dt * 1000
            return

        # Check for collision with enemies or enemy bullets (Immediate Game Over)
        hits = pygame.sprite.spritecollide(self.game.player, self.enemies, False)
        bullet_hits = pygame.sprite.spritecollide(self.game.player, self.enemy_bullets, True)
        
        if hits or bullet_hits:
            from .game_over_scene import GameOverScene
            print("Collision detected! Game Over triggered.")
            self.manager.change(GameOverScene(self.manager))
            return 
            
        # Bullet - Enemy collision
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        if hits:
            print("Enemy defeated!")
            
        # Check for victory / level completion
        if len(self.enemies) == 0 and not self.transitioning:
            # Initialize transition timer if not set
            if not hasattr(self, 'transition_delay'):
                self.transition_delay = 1000 # 1 second delay
            
            self.transition_delay -= dt * 1000
            
            if self.transition_delay <= 0:
                import json
                config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'levels.json')
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    levels = data['levels']
                    next_level = next((l for l in levels if l['id'] == self.level_id + 1), None)
                    
                self.transitioning = True
                if next_level:
                    print(f"Level {self.level_id} cleared! Loading Level {next_level['id']}...")
                    from .loading_scene import LoadingScene
                    self.manager.change(LoadingScene(self.manager, next_level['id']))
                    return
                else:
                    from .victory_scene import VictoryScene
                    self.manager.change(VictoryScene(self.manager))
                    return

    def draw(self, screen):
        screen.fill(BLACK)
        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))
