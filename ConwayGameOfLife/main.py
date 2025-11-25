import re
import os
import glob

from gameoflife.rulesmanager import RULE_SETS
from gameoflife.gol import GameOfLife
from gameoflife.rules import register_rule_set

# Import new custom rule 'chaoslife' apart from the existing rules
@register_rule_set('chaoslife')
def apply_chaos_life_rules(cell_state, live_neighbors):
    """
    Applies 'ChaosLife' rules: a cell is born if it has 1 or 5 neighbors,
    and a live cell always dies.
    """
    if cell_state == 1:  # Live cell always dies
        return 0
    else:  # Dead cell born if 1 or 5 neighbors
        if live_neighbors == 1 or live_neighbors == 5:
            return 1
        else:
            return 0

# Read the dimension from the user in the format (row, column)
user_input = input("Enter the dimension of the grid in the format '(row,column)', like as, (5,6): ")
pattern = r'^\(\s*(\d+)\s*,\s*(\d+)\s*\)$'
match = re.match(pattern, user_input)
if not match:
   # print("Invalid format. Enter range within braces eg (5,5)")
    raise ValueError("Input must match the format (row,column), e.g., (3,5)")
row, column = map(int, match.groups())
    

print("##################################")
print("Available rules: ")
index = 1
rule_name = ''
available_rules = []
for rule in RULE_SETS:
    print(index, '. ', rule)
    available_rules.append(rule)
    index = index + 1
print("##################################")

rule_index = int(input("Enter the choice of the rule set that need to be applied': "))
if rule_index > len(available_rules) or rule_index < 1:
    print("Invalid. Specify range within 1-4.")
   # raise ValueError(f"Rule specified with index - '{rule_index}' does not exist. "
                    # f"Available rules: {', '.join(RULE_SETS.keys())}")
    exit(1)

rule_name = available_rules[rule_index - 1]
print("Using the provided rule: ", rule_name)
game = GameOfLife(row, column, rule_set_name=rule_name)

# Load pattern from file
pattern_filename = "pattern.txt"
if not os.path.isfile(pattern_filename):
    raise FileNotFoundError(f"Pattern file not found: {pattern_filename}")

game.load_pattern_from_file(pattern_filename)

print(f"Loaded the pattern file {pattern_filename}")

max_generations = int(input("Enter the number of generations to update: "))

# Ensure output folder is clean
current_dir = os.getcwd()
pattern = os.path.join(os.getcwd(), f"grid_state_gen*.txt")

# Delete old matching files
for f in glob.glob(pattern):
    os.remove(f)

for gen in range(1, max_generations + 1):
    game.update_grid()
    filename = f"grid_state_gen{gen}.txt"
    game.save_grid_to_file(filename)
    print(f"\nGrid State after {gen} update(s):\n", game.grid)