import pytest
import pygame
import os
import sys

# Add src to path so we can import things
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    # Setup headless mode for tests
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    yield
    pygame.quit()

@pytest.fixture
def mock_game():
    class MockGame:
        def __init__(self):
            from src.engine.resource_manager import ResourceManager
            self.resource_manager = ResourceManager()
            self.dt = 0.016
            self.clock = pygame.time.Clock()
    return MockGame()
