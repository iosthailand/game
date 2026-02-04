import json
import os
import pygame
import random
from settings import *
from ..entities.player import Player
from ..entities.enemy import Slime, Ghost, FastEnemy, GoblinArcher, Wizard
from ..entities.decoration import Decoration
from ..utils.map_loader import Tile

class SpawnManager:
    def __init__(self, game):
        self.game = game
        self.enemy_classes = {
            "Slime": Slime,
            "Ghost": Ghost,
            "FastEnemy": FastEnemy,
            "GoblinArcher": GoblinArcher,
            "Wizard": Wizard
        }
        self.enemy_definitions = self.load_definitions()

    def load_definitions(self):
        try:
            path = os.path.join(self.game.resource_manager.base_path, 'data', 'enemy_definitions.json')
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading enemy definitions: {e}")
            return {}

    def spawn_tile(self, scene, col, row):
        return Tile(scene, col, row)

    def spawn_player(self, scene, x, y):
        player = Player(scene, x, y)
        self.game.player = player
        return player

    def spawn_enemies(self, scene, map_data, level_config):
        # Spawn Decorations first (so they are drawn behind)
        self.spawn_decorations(scene, map_data, level_config)
        
        enemies_config = level_config['enemies']
        
        # Parse enemy configuration
        enemy_data = [] # List of tuples: (class, weight, sprite_sheet, scale)
        
        for enemy_entry in enemies_config:
            if isinstance(enemy_entry, str):
                # Old format: equal distribution
                enemy_type = enemy_entry
                if enemy_type in self.enemy_classes:
                    # Get default properties from definitions
                    def_data = self.enemy_definitions.get(enemy_type, {})
                    sprite_sheet = def_data.get('sprite_sheet')
                    scale = def_data.get('scale', 1.0)
                    enemy_data.append((self.enemy_classes[enemy_type], 1, sprite_sheet, scale))
            elif isinstance(enemy_entry, dict):
                # New format: percentage-based
                enemy_type = enemy_entry.get('type')
                percentage = enemy_entry.get('percentage', 0)
                if enemy_type in self.enemy_classes and percentage > 0:
                    # Level config can override sprite sheet and scale
                    def_data = self.enemy_definitions.get(enemy_type, {})
                    
                    sprite_sheet = enemy_entry.get('sprite_sheet')
                    if not sprite_sheet:
                        sprite_sheet = def_data.get('sprite_sheet')
                        
                    scale = enemy_entry.get('scale')
                    if scale is None:
                        scale = def_data.get('scale', 1.0)
                    
                    enemy_data.append((self.enemy_classes[enemy_type], percentage, sprite_sheet, scale))
        
        # Fallback to Slime if no valid enemies
        if not enemy_data:
            enemy_data = [(Slime, 1, 'enemy_slime.png', 1.0)]

        # Separate into components for random.choices
        choices_data = [(d[0], d[2], d[3]) for d in enemy_data]
        weights = [d[1] for d in enemy_data]

        # Spawn enemies using weighted random selection
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'E' or (tile == '.' and random.random() < level_config['encounter_rate']):
                    choice = random.choices(choices_data, weights=weights, k=1)[0]
                    enemy_class, sprite_sheet, scale = choice
                    
                    # Pass sprite_sheet and scale to class
                    kwargs = {}
                    if sprite_sheet:
                        kwargs['sprite_sheet'] = sprite_sheet
                    if scale is not None:
                        kwargs['scale'] = scale
                        
                    e = enemy_class(scene, col * TILESIZE, row * TILESIZE, **kwargs)
                        
                    scene.all_sprites.add(e)
                    scene.enemies.add(e)

    def spawn_decorations(self, scene, map_data, level_config):
        bg_config = level_config.get('background', {})
        decos = bg_config.get('decorations', [])
        
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                # Only spawn on floor tiles
                if tile == '.':
                    for deco in decos:
                        if random.random() < deco.get('density', 0):
                            d = Decoration(scene, col * TILESIZE, row * TILESIZE, deco['asset'], (scene.all_sprites, scene.decorations))
                            # We don't add to enemies or walls
                            break # One deco per tile max
