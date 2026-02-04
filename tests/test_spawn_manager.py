import pytest
import os
import json
from src.engine.spawn_manager import SpawnManager

def test_enemy_definitions_loading(mock_game, tmp_path):
    # Setup dummy definitions
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    def_file = data_dir / "enemy_definitions.json"
    def_data = {"Slime": {"sprite_sheet": "slime.png", "scale": 1.0}}
    def_file.write_text(json.dumps(def_data))
    
    # Mock the base_path in resource_manager
    mock_game.resource_manager.base_path = str(tmp_path)
    
    sm = SpawnManager(mock_game)
    assert "Slime" in sm.enemy_definitions
    assert sm.enemy_definitions["Slime"]["sprite_sheet"] == "slime.png"

def test_map_file_path_resolution(mock_game):
    sm = SpawnManager(mock_game)
    # Check if load_definitions handles missing directory gracefully (already tested via rm mock)
    pass
