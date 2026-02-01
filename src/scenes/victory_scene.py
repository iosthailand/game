import pygame
from settings import *
from .base_scene import BaseScene

class VictoryScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont("Arial", 64, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 32)
        self.input_cooldown = 2000 # 2 seconds delay before input is accepted
        
    def handle_events(self, events):
        # Ignore input during cooldown
        if self.input_cooldown > 0:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_r:
                    # Restart game
                    self.game.player.health = 100
                    from .loading_scene import LoadingScene
                    self.manager.change(LoadingScene(self.manager))
                if event.key == pygame.K_ESCAPE:
                    self.game.quit()

    def update(self, dt):
        if self.input_cooldown > 0:
            self.input_cooldown -= dt * 1000

    def draw(self, screen):
        screen.fill(BGCOLOR)
        
        # Victory message
        victory_text = self.font.render("VICTORY!", True, YELLOW)
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - 100))
        
        # Message
        msg_text = self.small_font.render("You have defeated all enemies!", True, WHITE)
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT // 2))
        
        # Instructions - Only show when input is available
        if self.input_cooldown <= 0:
            instr_text = self.small_font.render("Press SPACE to Restart or ESC to Quit", True, LIGHTGREY)
            screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 2 + 100))
