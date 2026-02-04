import pytest
import pygame
from src.engine.resource_manager import ResourceManager

def test_image_placeholder_creation(tmp_path):
    rm = ResourceManager()
    rm.base_path = str(tmp_path)
    # Ensure assets/graphics exists or rm handles it
    # Loading a non-existent image should return a magenta placeholder
    img = rm.load_image("missing", "non_existent_file.png")
    assert isinstance(img, pygame.Surface)
    assert img.get_at((0, 0)) == (255, 0, 255, 255) # Magenta

def test_font_caching():
    rm = ResourceManager()
    f1 = rm.load_font("Arial", 32)
    f2 = rm.load_font("Arial", 32)
    assert f1 is f2 # Should be the same object

def test_sound_loading_interface(mock_game, tmp_path):
    # This test checks if load_sound handles missing files gracefully
    rm = mock_game.resource_manager
    rm.base_path = str(tmp_path)
    snd = rm.load_sound("missing_sound", "no_sound.wav")
    assert snd is None
