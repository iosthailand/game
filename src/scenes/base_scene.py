import pygame

class BaseScene:
    def __init__(self, manager):
        self.manager = manager
        self.game = manager.game

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
