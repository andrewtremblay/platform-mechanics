"""
Color class.

Contains all the colors used in the exaples as a giant enum.
"""

from enum import Enum


class Color(Enum):
    """Container for common colors."""

    Black = (0, 0, 0)
    White = (255, 255, 255)
    Green = (0, 255, 0)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
