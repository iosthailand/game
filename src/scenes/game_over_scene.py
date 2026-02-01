import pygame
import sys
from settings import *
from .base_scene import BaseScene

class GameOverScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        # Using larger, bolder fonts for a premium feel
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 32)
        self.start_ticks = pygame.time.get_ticks()
        print("SCENE: GameOverScene Active")
        
    def handle_events(self, events):
        # 500ms safety delay
        if pygame.time.get_ticks() - self.start_ticks < 500:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game.player:
                        self.game.player.health = 100
                    from .loading_scene import LoadingScene
                    self.manager.change(LoadingScene(self.manager, 1))
                    return
                    
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update(self, dt):
        pass

    def draw(self, screen):
        # Pitch black background for focus
        screen.fill((10, 10, 10))
        
        # Calculate blinking pulse
        pulse = (pygame.time.get_ticks() // 500) % 2 == 0
        
        # Title: Game Over (Red with slight pulse effect or just bright)
        over_text = self.title_font.render("Game Over", True, RED)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 120))
        
        # press <Space> Play Game
        play_color = WHITE if pulse else LIGHTGREY
        play_text = self.small_font.render("press <Space> Play Game", True, play_color)
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 + 30))
        
        # press <Esc> Quit Game
        quit_text = self.small_font.render("press <Esc> Quit Game", True, (150, 150, 150))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 90))
        
        # Subtle border to match professional UI look (optional)
        pygame.draw.rect(screen, RED, (WIDTH // 2 - 250, HEIGHT // 2 - 160, 500, 320), 2)
