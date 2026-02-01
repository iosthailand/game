import pygame
import sys
from settings import *
from src.engine.scene_manager import SceneManager
from src.engine.resource_manager import ResourceManager
from src.scenes.loading_scene import LoadingScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.dt = 0
        
        # Managers
        self.resource_manager = ResourceManager()
        from src.engine.spawn_manager import SpawnManager
        self.spawn_manager = SpawnManager(self)
        self.scene_manager = SceneManager(self)
        
        # Initial Scene
        self.current_scene = None
        self.scene_manager.change(LoadingScene(self.scene_manager, 1))

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
        self.scene_manager.handle_events(events)

    def update(self):
        self.scene_manager.update(self.dt)

    def draw(self):
        self.scene_manager.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    g = Game()
    g.run()
