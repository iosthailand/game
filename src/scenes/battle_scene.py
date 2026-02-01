import pygame
import random
from settings import *
from .base_scene import BaseScene

class BattleScene(BaseScene):
    def __init__(self, manager, enemy):
        super().__init__(manager)
        self.font = pygame.font.SysFont("Arial", 32)
        self.enemy = enemy
        # Load enemy health if available, else default
        self.enemy_hp = enemy.health if hasattr(enemy, 'health') else 50
        print(f"Entering Battle with {enemy.__class__.__name__}")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Attack
                    self.player_attack()
                    return # Consume event and stop frame processing for this scene
                
                if event.key == pygame.K_ESCAPE:
                    self.manager.pop()
                    return

    def player_attack(self):
        damage = 10
        self.enemy_hp -= damage
        print(f"Attacked Enemy! HP left: {self.enemy_hp}")
        
        if self.enemy_hp <= 0:
            print("Victory!")
            self.enemy.kill() # Remove from world
            self.manager.pop()
        else:
            # Enemy attacks back
            self.enemy_attack()

    def enemy_attack(self):
        damage = random.randint(5, 15)
        self.game.player.health -= damage
        print(f"Enemy attacked you! Damage: {damage}, HP left: {self.game.player.health}")
        
        if self.game.player.health <= 0:
            print("You died!")
            # Use local import and change scene
            from .game_over_scene import GameOverScene
            self.manager.change(GameOverScene(self.manager))
            return

    def update(self, dt):
        pass

    def draw(self, screen):
        # If player is dead, don't draw victory/battle UI
        if self.game.player.health <= 0:
            return

        screen.fill(DARKGREY)
        text = self.font.render("BATTLE - Press SPACE to Attack, ESC to Run", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        
        enemy_text = self.font.render(f"Enemy HP: {self.enemy_hp}", True, RED)
        screen.blit(enemy_text, (WIDTH // 2 - enemy_text.get_width() // 2, HEIGHT // 2 + 10))
        
        player_text = self.font.render(f"Your HP: {self.game.player.health}", True, BLUE)
        screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, HEIGHT // 2 + 50))
