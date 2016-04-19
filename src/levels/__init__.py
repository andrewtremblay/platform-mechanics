"""
Levels module.

The levels package contains the level data as well as the level components.
"""
from .level_01 import Level_01


def build_levels(player):
    """Return all levels for the main game loop."""
    level_list = []
    level_list.append(Level_01(player))
    return level_list
