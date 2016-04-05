from enum import Enum

class JumpState(Enum):
    grounded = 0
    crouching = 1
    jumping = 2
    falling = 3
    landing = 4
