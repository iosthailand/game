import pytest
import os
from src.utils.map_loader import Map

def test_map_parsing(tmp_path):
    # Create a dummy map file
    map_data = "111\n1P1\n111"
    map_file = tmp_path / "test_map.txt"
    map_file.write_text(map_data)
    
    # In map_loader.py, TILESIZE is used. We need to make sure settings is accessible.
    from settings import TILESIZE
    
    m = Map(str(map_file))
    
    assert m.tilewidth == 3
    assert m.tileheight == 3
    assert m.width == 3 * TILESIZE
    assert m.height == 3 * TILESIZE
    assert m.data[1][1] == 'P'

def test_map_empty_file_handling(tmp_path):
    map_file = tmp_path / "empty.txt"
    map_file.write_text("")
    
    with pytest.raises(Exception):
        Map(str(map_file))
