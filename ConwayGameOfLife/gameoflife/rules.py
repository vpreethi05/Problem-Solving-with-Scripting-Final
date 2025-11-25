from .rulesmanager import register_rule_set

@register_rule_set('conway')
def apply_conway_rules(cell_state, live_neighbors):
    """
    Applies Conway's Game of Life rules to determine the next state of a cell.
    """
    if cell_state == 1:  # Live cell
        if live_neighbors < 2 or live_neighbors > 3:
            return 0  # Underpopulation or overpopulation: dies
        else:
            return 1  # Lives on to the next generation
    else:  # Dead cell
        if live_neighbors == 3:
            return 1  # Reproduction: becomes a live cell
        else:
            return 0  # Remains dead

@register_rule_set('highlife')
def apply_highlife_rules(cell_state, live_neighbors):
    """
    Applies HighLife rules to determine the next state of a cell.
    Born if has 3 or 6 neighbors, survives if 2 or 3 neighbors.
    """
    if cell_state == 1:  # Live cell
        if live_neighbors == 2 or live_neighbors == 3:
            return 1  # Survives
        else:
            return 0  # Dies
    else:  # Dead cell
        if live_neighbors == 3 or live_neighbors == 6:
            return 1  # Born
        else:
            return 0  # Remains dead

@register_rule_set('superlife')
def apply_superlife_rules(cell_state, live_neighbors):
    """
    Applies SuperLife rules to determine the next state of a cell.
    Born if has 3, 2, 4, 5, 8, 7, or 6 neighbors, survives if 2, 3, or 8 neighbors.
    """
    if cell_state == 1:  # Live cell
        if live_neighbors == 2 or live_neighbors == 3 or live_neighbors == 8:
            return 1  # Survives
        else:
            return 0  # Dies
    else:  # Dead cell
        if live_neighbors in [3, 2, 4, 5, 8, 7, 6]:
            return 1  # Born
        else:
            return 0  # Remains dead