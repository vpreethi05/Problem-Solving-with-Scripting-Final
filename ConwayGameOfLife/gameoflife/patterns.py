import re

def load_pattern_from_string(game_instance, pattern_data_string):
    """
    Parses a string containing coordinate pairs and sets the corresponding cells to live
    in the provided game_instance's grid.
    Expected format: '(row,col) (row,col) ...'
    """
    coordinates = re.findall(r'\((\d+),(\d+)\)', pattern_data_string)

    for row_str, col_str in coordinates:
        row, col = int(row_str), int(col_str)
        if 0 <= row < game_instance.rows and 0 <= col < game_instance.cols:
            game_instance.grid[row, col] = 1
        else:
            print(f"Warning: Coordinate ({row},{col}) is out of grid bounds for {game_instance.rows}x{game_instance.cols} grid.")
    print(f"Pattern loaded from string: {pattern_data_string}")

def load_pattern_from_file(game_instance, filepath):
    """
    Loads a pattern from a specified file and applies it to the game_instance's grid.
    The file content is expected to be in the format parsable by load_pattern_from_string.
    """
    try:
        with open(filepath, 'r') as f:
            pattern_string = f.read().strip()
        load_pattern_from_string(game_instance, pattern_string)
        print(f"Pattern successfully loaded from file: {filepath}")
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred while loading pattern from file {filepath}: {e}")