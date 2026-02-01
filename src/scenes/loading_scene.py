import pygame
from settings import *
from .base_scene import BaseScene

class LoadingScene(BaseScene):
    def __init__(self, manager, next_level_id=1):
        super().__init__(manager)
        self.font = pygame.font.SysFont("Arial", 48)
        self.next_level_id = next_level_id
        self.timer = 0
        self.duration = 1000 # 1 second for a smooth feel
        print(f"Loading Level {next_level_id}...")

    def update(self, dt):
        self.timer += dt * 1000
        if self.timer >= self.duration:
            from .world_scene import WorldScene
            # We change exactly once when duration is met
            self.manager.change(WorldScene(self.manager, self.next_level_id))

    def draw(self, screen):
        screen.fill(BLACK)
        text = self.font.render(f"PREPARING LEVEL {self.next_level_id}... {min(100, int(self.timer / self.duration * 100))}%", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        
        # Simple loading bar
        bar_width = 400
        bar_height = 20
        pygame.draw.rect(screen, LIGHTGREY, (WIDTH // 2 - bar_width // 2, HEIGHT // 2 + 50, bar_width, bar_height), 2)
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - bar_width // 2, HEIGHT // 2 + 50, int(bar_width * (self.timer / self.duration)), bar_height))
