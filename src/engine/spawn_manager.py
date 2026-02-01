import pygame
import random
from settings import *
from ..entities.player import Player
from ..entities.enemy import Slime, Ghost, FastEnemy
from ..utils.map_loader import Tile

class SpawnManager:
    def __init__(self, game):
        self.game = game
        self.enemy_classes = {
            "Slime": Slime,
            "Ghost": Ghost,
            "FastEnemy": FastEnemy
        }

    def spawn_tile(self, scene, col, row):
        return Tile(scene, col, row)

    def spawn_player(self, scene, x, y):
        player = Player(scene, x, y)
        self.game.player = player
        return player

    def spawn_enemies(self, scene, map_data, level_config):
        available_enemies = [
            self.enemy_classes[name] 
            for name in level_config['enemies'] 
            if name in self.enemy_classes
        ]
        
        if not available_enemies:
            available_enemies = [Slime]

        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'E' or (tile == '.' and random.random() < level_config['encounter_rate']):
                    enemy_type = random.choice(available_enemies)
                    e = enemy_type(scene, col * TILESIZE, row * TILESIZE)
                    scene.all_sprites.add(e)
                    scene.enemies.add(e)
