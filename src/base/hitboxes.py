"""
Hitboxes module.

Common hitboxes used around the project.
"""
import config


class HITBOX:
    """Common hitboxes."""

    BOTTOM_SCREEN = [config.SCREEN_WIDTH,
                     config.PLAYER.INITIAL.HEIGHT,
                     0,
                     config.SCREEN_HEIGHT]
