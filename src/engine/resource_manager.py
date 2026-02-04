import pygame
import os

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def load_image(self, name, path):
        full_path = os.path.join(self.base_path, 'assets', 'graphics', path)
        if name not in self.images:
            try:
                self.images[name] = pygame.image.load(full_path).convert_alpha()
            except Exception as e:
                print(f"Warning: Could not load image {path}. Error: {e}")
                # Create a placeholder if file not found
                surf = pygame.Surface((32, 32))
                surf.fill((255, 0, 255)) # Magenta placeholder
                self.images[name] = surf
        return self.images[name]

    def get_image(self, name):
        return self.images.get(name)

    def load_font(self, name, size):
        key = f"{name}_{size}"
        if key not in self.fonts:
            self.fonts[key] = pygame.font.SysFont(name, size)
        return self.fonts[key]

    def load_sound(self, name, path, volume=1.0):
        full_path = os.path.join(self.base_path, 'assets', 'audio', path)
        if name not in self.sounds:
            try:
                sound = pygame.mixer.Sound(full_path)
                sound.set_volume(volume)
                self.sounds[name] = sound
            except Exception as e:
                print(f"Warning: Could not load sound {path}. Error: {e}")
                return None
        return self.sounds[name]

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Warning: Sound {name} not found in cache")

    def get_spritesheet_frames(self, name, frame_width, frame_height):
        sheet = self.get_image(name)
        if not sheet:
            return []
        
        frames = []
        rows = sheet.get_height() // frame_height
        cols = sheet.get_width() // frame_width
        
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), rect)
                frames.append(frame)
        return frames
