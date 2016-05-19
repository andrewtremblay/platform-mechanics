"""
Configs package.

A container holding constants that other packages share.
"""

from .world import WORLD


class PlayerConfig:
    """Player constants."""

    # TODO: have the jump decay be different from base gravity
    JUMP_DECAY = WORLD.GRAVITY

    # the delay (in ticks) between pressing jump and activating
    # the regular jump if the jump is released during this delay,
    # CROUCH_JUMP_SPEED will be used instead
    CROUCH_DELAY = 50

    # Initial values
    class INITIAL:
        WIDTH = 40  # width of the player base sprite
        HEIGHT = 60  # height of the player base sprite
        FULL_HOP_JUMP_SPEED = -12 # a regular hold-button-to-jump jump
        SHORT_HOP_JUMP_SPEED = -6  # used when jumping right out of a crouch

    # Movement (only horizontal right now)
    class MOVE:
        HORIZ_SPEED = 6  # walking left and right in both air and on platorms

    # Max values
    class MAX:
        BASE_FALL_SPEED = 12  # can't fall faster than this
        BASE_JUMP_SPEED = -12  # can't jump up faster than this

PLAYER = PlayerConfig()
