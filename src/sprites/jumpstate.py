"""The state of a sprites jump."""
from enum import Enum


class JumpState(Enum):
    """Also known as "leg state"."""

    grounded = 0
    crouching = 1
    jumping = 2
    falling = 3
    landing = 4


def toStr(x):
    """Create a string from the given state."""
    return {
        JumpState.grounded:     'grounded',
        JumpState.crouching:    'crouching',
        JumpState.jumping:      'jumping',
        JumpState.falling:      'falling',
        JumpState.landing:      'landing',
    }[x]
