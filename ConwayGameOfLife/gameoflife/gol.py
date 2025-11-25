import numpy as np

# Import the new modules
from gameoflife.patterns import load_pattern_from_string, load_pattern_from_file
from gameoflife.save import save_grid_to_file
from gameoflife.rulesmanager import RULE_SETS

class GameOfLife:
    def __init__(self, rows, cols, rule_set_name='conway'):
        """
        Initializes the Game of Life grid with specified dimensions.
        All cells are initially dead.
        """
        # Add validation for rows and cols (Instruction 1)
        if not isinstance(rows, int) or not isinstance(cols, int) or rows <= 0 or cols <= 0:
            raise ValueError("Grid dimensions (rows, cols) must be positive integers.")

        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        print(f"Game of Life grid initialized with dimensions {self.rows}x{self.cols}.")
        if rule_set_name in RULE_SETS:
            self.current_rule_set = RULE_SETS[rule_set_name]
            print(f"Game of Life grid initialized with dimensions {self.rows}x{self.cols} using '{rule_set_name}' rules.")
        else:
            raise ValueError(f"Unknown rule set: {rule_set_name}. Available rule sets: {list(RULE_SETS.keys())}")

    def _count_live_neighbors(self, row, col):
        """
        Counts the number of live neighbors for a given cell.
        Handles boundary conditions.
        """
        live_neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue # Don't count the cell itself

                neighbor_row, neighbor_col = row + i, col + j

                # Check boundary conditions
                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    live_neighbors += self.grid[neighbor_row, neighbor_col]
        return live_neighbors

    def update_grid(self):
        """
        Updates the grid to the next generation based on Game of Life rules.
        A new grid is created to avoid affecting neighbor counts for the current generation.
        """
        new_grid = np.copy(self.grid) # Create a copy to store the next state

        for r in range(self.rows):
            for c in range(self.cols):
                live_neighbors = self._count_live_neighbors(r, c)
                current_state = self.grid[r, c]
                # Use the imported apply_conway_rules function
                new_grid[r, c] = self.current_rule_set(current_state, live_neighbors)
        self.grid = new_grid
        print("Grid updated to the next generation.")

    def load_pattern_from_string(self, pattern_data_string):
        """
        Wrapper for the external load_pattern_from_string function.
        """
        load_pattern_from_string(self, pattern_data_string)

    def load_pattern_from_file(self, filepath):
        """
        Wrapper for the external load_pattern_from_file function.
        """
        load_pattern_from_file(self, filepath)

    def save_grid_to_file(self, filepath):
        """
        Wrapper for the external save_grid_to_file function.
        """
        save_grid_to_file(self, filepath)

    def run_simulation(self, num_generations):
        # Simplified run_simulation for testing, focusing on state changes
        for gen in range(num_generations):
            self.update_grid()
