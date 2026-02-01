import pygame
import random
from settings import *
from ..entities.player import Player
from ..entities.enemy import Slime, Ghost, FastEnemy, GoblinArcher, Wizard
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

    def spawn_tile(self, scene, col, row):
        return Tile(scene, col, row)

    def spawn_player(self, scene, x, y):
        player = Player(scene, x, y)
        self.game.player = player
        return player

    def spawn_enemies(self, scene, map_data, level_config):
        enemies_config = level_config['enemies']
        
        # Parse enemy configuration (supports both old and new formats)
        enemy_types = []
        weights = []
        
        for enemy_entry in enemies_config:
            if isinstance(enemy_entry, str):
                # Old format: equal distribution
                if enemy_entry in self.enemy_classes:
                    enemy_types.append(self.enemy_classes[enemy_entry])
                    weights.append(1)
            elif isinstance(enemy_entry, dict):
                # New format: percentage-based
                enemy_type = enemy_entry.get('type')
                percentage = enemy_entry.get('percentage', 0)
                if enemy_type in self.enemy_classes and percentage > 0:
                    enemy_types.append(self.enemy_classes[enemy_type])
                    weights.append(percentage)
        
        # Fallback to Slime if no valid enemies
        if not enemy_types:
            enemy_types = [Slime]
            weights = [1]

        # Spawn enemies using weighted random selection
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'E' or (tile == '.' and random.random() < level_config['encounter_rate']):
                    enemy_class = random.choices(enemy_types, weights=weights, k=1)[0]
                    e = enemy_class(scene, col * TILESIZE, row * TILESIZE)
                    scene.all_sprites.add(e)
                    scene.enemies.add(e)
