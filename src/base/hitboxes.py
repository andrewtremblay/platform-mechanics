"""
Hitboxes module.

Common hitboxes used around the project.
"""
import configs as conf


class HITBOX:
    """Common hitboxes."""

    BOTTOM_SCREEN = [conf.UI.SCREEN_WIDTH,
                     conf.PLAYER.INITIAL.HEIGHT,
                     0,
                     conf.UI.SCREEN_HEIGHT]
