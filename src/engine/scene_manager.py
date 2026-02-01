import pygame

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scenes = []

    def push(self, scene):
        print(f"Pushing scene: {scene.__class__.__name__}")
        self.scenes.append(scene)

    def pop(self):
        if self.scenes:
            removed = self.scenes.pop()
            print(f"Popped scene: {removed.__class__.__name__}")

    def change(self, scene):
        print(f"Changing scene to: {scene.__class__.__name__}")
        self.scenes = [scene]

    def handle_events(self, events):
        if self.scenes:
            self.scenes[-1].handle_events(events)

    def update(self, dt):
        if self.scenes:
            self.scenes[-1].update(dt)

    def draw(self, screen):
        if self.scenes:
            self.scenes[-1].draw(screen)
