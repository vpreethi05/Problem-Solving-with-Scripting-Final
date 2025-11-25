import os
import glob

def save_grid_to_file(game_instance, filepath):
    """
    Saves the current state of the grid to a file.
    """
    # Now save normally
    try:
        with open(filepath, 'w') as f:
            for r in range(game_instance.rows):
                line = ''.join(['1' if cell == 1 else '0' for cell in game_instance.grid[r, :]])
                f.write(line + '\n')
        print(f"Grid state successfully saved to file: {filepath}")
    except Exception as e:
        print(f"An error occurred while saving grid to file {filepath}: {e}")
