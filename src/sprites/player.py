"""
Player class.

Player contains all behavior related to the player sprite. This
 includes some logic related to the controller though most of that
 is delegated to its own class.
"""
import pygame

from base.color import Color
from debug import DEBUG
import configs as conf
from configs import PLAYER as P

from .jumpstate import JumpState


class Player(pygame.sprite.Sprite):
    """Represents the sprite that the player controls."""

    def __init__(self):
        """Construct the sprite."""
        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = P.INITIAL.WIDTH
        height = P.INITIAL.HEIGHT
        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Red.value)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set initial speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None
        DEBUG.Log("set grounded jump_state (init)")
        self.jump_state = JumpState.grounded
        self.DEBUG_PREV_JUMP_STATE = self.jump_state

    def update(self):
        """Determine sprite position, jump_state, and speed."""
        # > crouching > jumping > falling > landing
        if (self.jump_state == JumpState.crouching and
                self.crouching_ticks < pygame.time.get_ticks()):
            # we've run out of time, start jumping
            self.jump_state = JumpState.jumping
            self.change_y = P.INITIAL.FULL_HOP_JUMP_SPEED
        else:
            # Gravity
            self.calc_grav()
            # Move left/right
            self.rect.x += self.change_x
            # See if we hit anything
            block_hit_list = pygame.sprite.spritecollide(
                self, self.level.platform_list, False)
            for block in block_hit_list:
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
            # Move up/down
            self.rect.y += self.change_y
            # Check and see if we hit anything
            block_hit_list = pygame.sprite.spritecollide(
                self, self.level.platform_list, False)
            for block in block_hit_list:
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    DEBUG.Log("set grounded jump_state (update)")
                    self.jump_state = JumpState.grounded
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                self.change_y = 0
        # handle debug jump state
        if self.DEBUG_PREV_JUMP_STATE != self.jump_state:
            DEBUG.Log("jump state change " + self.jump_state.name)
            self.DEBUG_PREV_JUMP_STATE = self.jump_state

    def calc_grav(self):
        """Calculate effect of gravity."""
        # but override all this if we're on a platform
        if self.is_on_platform():
            # self.jump_state == JumpState.jumping or
            # self.rect.y = self.rect.y - 1
            # if we are crouching on the ground.
            if(self.jump_state == JumpState.crouching):
                if(self.crouching_ticks < pygame.time.get_ticks()):
                    # apply default jump
                    self.jump_state = JumpState.jumping
                    self.change_y = P.SHORT_HOP_JUMP_SPEED
            elif(self.jump_state == JumpState.grounded):
                self.change_y = 0
            else:
                # if we are not crouching or grounding then
                # we are falling, landing, or grounding
                # log.Debug("set grounded jump_state (calc_grav)")
                self.jump_state = JumpState.grounded
        else:
            if self.change_y > 0:
                self.jump_state = JumpState.falling
            self.change_y += P.JUMP_DECAY
        # clamp the y parameters
        self.change_y = min(self.change_y, P.MAX.BASE_FALL_SPEED)
        self.change_y = max(self.change_y, P.MAX.BASE_JUMP_SPEED)

    def is_on_platform(self):
        """check whether sprite is on a platform."""
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False)
        self.rect.y -= 2
        return ((len(platform_hit_list) > 0 or
                self.rect.bottom >= conf.UI.SCREEN_HEIGHT) and
                self.jump_state != JumpState.jumping)

    def jump_pressed(self):
        """Called on the frame when the user presses 'jump' button."""
        DEBUG.Log("jump_pressed")
        if self.jump_state == JumpState.grounded:
            self.jump_state = JumpState.crouching
            self.crouching_ticks = pygame.time.get_ticks() + P.CROUCH_DELAY
        else:
            DEBUG.Log("no jump")

    def jump_released(self):
        """Called on the frame when the user releases 'jump' button."""
        if self.jump_state == JumpState.crouching:
            self.jump_state = JumpState.jumping
            self.change_y = P.INITIAL.SHORT_HOP_JUMP_SPEED

    # Player-controlled movement:
    def go_left(self):
        """Called when the user hits the left arrow."""
        self.change_x = -(P.MOVE.HORIZ_SPEED)

    def go_right(self):
        """Called when the user hits the right arrow."""
        self.change_x = (P.MOVE.HORIZ_SPEED)

    def stop(self):
        """Called when the user lets off the keyboard."""
        self.change_x = 0
