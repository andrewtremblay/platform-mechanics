import pygame

from base import color
import config as conf
from .jumpstate import JumpState


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(color.Color.Red.value)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

        self.jump_state = JumpState.grounded

    def update(self):
        if self.jump_state == JumpState.crouching and self.crouching_ticks < pygame.time.get_ticks(): # > crouching > jumping > falling > landing
            self.jump_state = JumpState.jumping
            self.change_y = -10


        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
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
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.jump_state = JumpState.grounded
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        #self.jump_state

        if self.change_y == 0:
            self.change_y = 1
        elif self.change_y < 0:
            self.change_y += .35
        elif self.change_y > 0:
            self.change_y += .35
            self.jump_state = JumpState.falling

        # See if we are on the ground.
        if self.rect.y >= conf.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = conf.SCREEN_HEIGHT - self.rect.height
            if self.jump_state != JumpState.crouching:
                self.jump_state = JumpState.grounded


    def is_on_platform(self):
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        # If it is ok to jump, set our speed upwards
        return (len(platform_hit_list) > 0 or self.rect.bottom >= conf.SCREEN_HEIGHT)



    def jump_pressed(self):
        """ Called when user hits 'jump' button. """
        if self.jump_state == JumpState.grounded:
            self.jump_state = JumpState.crouching
            self.crouching_ticks = pygame.time.get_ticks() + 50
        else:
            print("no jump")

    def jump_released(self):
        """ Called when user releases 'jump' button. """
        if self.jump_state == JumpState.crouching:
            self.change_y
        if self.change_y < 0:
            self.change_y = 0

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
