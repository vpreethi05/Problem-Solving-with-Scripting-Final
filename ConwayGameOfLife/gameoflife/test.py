import numpy as np
import pytest
import importlib

from .gol import GameOfLife
from .rules import apply_conway_rules, apply_highlife_rules

# Test GameOfLife Initialization
def test_gameoflife_init_valid_dimensions():
    game = GameOfLife(10, 10)
    assert game.rows == 10
    assert game.cols == 10
    assert np.all(game.grid == 0)
    assert game.current_rule_set == apply_conway_rules # Default rule set

def test_gameoflife_init_invalid_dimensions():
    with pytest.raises(ValueError, match="Grid dimensions .* must be positive integers."):
        GameOfLife(0, 10)
    with pytest.raises(ValueError, match="Grid dimensions .* must be positive integers."):
        GameOfLife(10, -5)
    with pytest.raises(ValueError, match="Grid dimensions .* must be positive integers."):
        GameOfLife(5.5, 10)

def test_gameoflife_init_custom_rule_set():
    game = GameOfLife(10, 10, rule_set_name='highlife')
    assert game.current_rule_set == apply_highlife_rules

def test_gameoflife_init_unknown_rule_set():
    with pytest.raises(ValueError, match="Unknown rule set"):
        GameOfLife(10, 10, rule_set_name='unknown_rules')

# Test _count_live_neighbors
def test_count_live_neighbors_center():
    game = GameOfLife(5, 5)
    game.grid[1:4, 1:4] = 1 # A 3x3 block of live cells
    game.grid[2,2] = 0 # Center cell is dead
    # All 8 neighbors are live for the center cell (2,2)
    assert game._count_live_neighbors(2, 2) == 8

def test_count_live_neighbors_corner():
    game = GameOfLife(3, 3)
    game.grid[0,1] = 1
    game.grid[1,0] = 1
    game.grid[1,1] = 1
    # Cell (0,0) has 3 live neighbors
    assert game._count_live_neighbors(0, 0) == 3

def test_count_live_neighbors_edge():
    game = GameOfLife(3, 3)
    game.grid[0,0] = 1
    game.grid[0,2] = 1
    game.grid[1,0] = 1
    game.grid[1,2] = 1
    game.grid[2,0] = 1
    game.grid[2,2] = 1
    # Cell (0,1) has 4 live neighbors with this setup
    assert game._count_live_neighbors(0, 1) == 4 # Corrected assertion

def test_count_live_neighbors_none():
    game = GameOfLife(5, 5)
    # Empty grid, no live neighbors anywhere
    assert game._count_live_neighbors(2, 2) == 0

# Test apply_conway_rules
def test_conway_rules_live_underpopulation():
    assert apply_conway_rules(1, 1) == 0

def test_conway_rules_live_survival():
    assert apply_conway_rules(1, 2) == 1
    assert apply_conway_rules(1, 3) == 1

def test_conway_rules_live_overpopulation():
    assert apply_conway_rules(1, 4) == 0

def test_conway_rules_dead_reproduction():
    assert apply_conway_rules(0, 3) == 1

def test_conway_rules_dead_no_reproduction():
    assert apply_conway_rules(0, 2) == 0
    assert apply_conway_rules(0, 4) == 0

# Test apply_highlife_rules
def test_highlife_rules_live_survival():
    assert apply_highlife_rules(1, 2) == 1
    assert apply_highlife_rules(1, 3) == 1

def test_highlife_rules_live_death():
    assert apply_highlife_rules(1, 1) == 0
    assert apply_highlife_rules(1, 4) == 0

def test_highlife_rules_dead_birth():
    assert apply_highlife_rules(0, 3) == 1
    assert apply_highlife_rules(0, 6) == 1

def test_highlife_rules_dead_no_birth():
    assert apply_highlife_rules(0, 2) == 0
    assert apply_highlife_rules(0, 4) == 0
    assert apply_highlife_rules(0, 5) == 0

# Test update_grid
def test_update_grid_blinker():
    game = GameOfLife(3, 3)
    game.grid = np.array([[0,0,0], [1,1,1], [0,0,0]])
    game.update_grid()
    expected_grid = np.array([[0,1,0], [0,1,0], [0,1,0]])
    assert np.array_equal(game.grid, expected_grid)

# Test load_pattern_from_string
def test_load_pattern_from_string_valid():
    game = GameOfLife(5, 5)
    pattern = "(0,1) (1,2) (2,0) (2,1) (2,2)"
    game.load_pattern_from_string(pattern)
    expected_grid = np.zeros((5,5), dtype=int)
    expected_grid[0,1] = 1
    expected_grid[1,2] = 1
    expected_grid[2,0] = 1
    expected_grid[2,1] = 1
    expected_grid[2,2] = 1
    assert np.array_equal(game.grid, expected_grid)

def test_load_pattern_from_string_out_of_bounds():
    game = GameOfLife(3, 3)
    pattern = "(0,0) (5,5)"
    game.load_pattern_from_string(pattern)
    expected_grid = np.zeros((3,3), dtype=int)
    expected_grid[0,0] = 1
    assert np.array_equal(game.grid, expected_grid)

def test_load_pattern_from_string_malformed():
    game = GameOfLife(3, 3)
    pattern = "(0,0) invalid_coord (1,1)"
    game.load_pattern_from_string(pattern)
    expected_grid = np.zeros((3,3), dtype=int)
    expected_grid[0,0] = 1
    expected_grid[1,1] = 1
    assert np.array_equal(game.grid, expected_grid)

# Test load_pattern_from_file
def test_load_pattern_from_file_valid(tmp_path):
    game = GameOfLife(5, 5)
    file_path = tmp_path / "valid_pattern.txt"
    file_path.write_text("(0,1) (1,2)")
    game.load_pattern_from_file(str(file_path))
    expected_grid = np.zeros((5,5), dtype=int)
    expected_grid[0,1] = 1
    expected_grid[1,2] = 1
    assert np.array_equal(game.grid, expected_grid)

def test_load_pattern_from_file_not_found():
    game = GameOfLife(5, 5)
    # Expect error message to be printed, grid should remain empty
    game.load_pattern_from_file("non_existent.txt")
    assert np.all(game.grid == 0)

def test_load_pattern_from_file_malformed(tmp_path):
    game = GameOfLife(3, 3)
    file_path = tmp_path / "malformed.txt"
    file_path.write_text("(0,0) invalid (1,1)")
    game.load_pattern_from_file(str(file_path))
    expected_grid = np.zeros((3,3), dtype=int)
    expected_grid[0,0] = 1
    expected_grid[1,1] = 1
    assert np.array_equal(game.grid, expected_grid)

# Test save_grid_to_file
def test_save_grid_to_file(tmp_path):
    game = GameOfLife(3, 3)
    game.grid[0,0] = 1
    game.grid[1,1] = 1
    game.grid[2,2] = 1
    file_path = tmp_path / "saved_grid.txt"
    game.save_grid_to_file(str(file_path))
    with open(file_path, 'r') as f:
        content = f.read()
    expected_content = "100\n010\n001\n"
    assert content == expected_content

# Test run_simulation (basic check for execution and grid changes)
def test_run_simulation_output(capsys):
    game = GameOfLife(3, 3)
    game.grid = np.array([[0,0,0], [1,1,1], [0,0,0]]) # Blinker pattern
    game.run_simulation(2)
    # For this test, we only check if the grid state is as expected after simulation.
    # The console output is not captured or asserted here to simplify.
    # Verify grid state after simulation (blinker should return to initial state after 2 generations)
    expected_grid_after_2_gens = np.array([[0,0,0], [1,1,1], [0,0,0]])
    assert np.array_equal(game.grid, expected_grid_after_2_gens)