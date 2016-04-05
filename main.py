"""Platform Mechanics.

Run all the classes together in one file for easier demoing.
"""
import sys
import pygame
from enum import Enum

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_BASE_FALL_SPEED = 12
MAX_BASE_JUMP_SPEED = -12
DEBUG_LOG_ENABLED = True  # False


class Color(Enum):
    """Container for common colors."""

    Black = (0, 0, 0)
    White = (255, 255, 255)
    Green = (0, 255, 0)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)


class JumpState(Enum):
    """Also known as "leg state"."""

    grounded = 0
    crouching = 1
    jumping = 2
    falling = 3
    landing = 4


def _jumpstate_tostr(x):
    return {
        JumpState.grounded: 'grounded',
        JumpState.crouching: 'crouching',
        JumpState.jumping: 'jumping',
        JumpState.falling: 'falling',
        JumpState.landing: 'landing',
    }[x]


class Player(pygame.sprite.Sprite):
    """Represents the sprite that the player controls."""

    # -- Methods
    def __init__(self):
        """Construct the sprite."""
        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Red.value)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None
        _debug_log("set grounded jump_state (init)")
        self.jump_state = JumpState.grounded
        self.DEBUG_PREV_JUMP_STATE = self.jump_state

    def update(self):
        """Determine sprite position, jump_state, and speed."""
        # > crouching > jumping > falling > landing
        if (self.jump_state == JumpState.crouching and
                self.crouching_ticks < pygame.time.get_ticks()):
            self.jump_state = JumpState.jumping
            self.change_y = -10
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
                    _debug_log("set grounded jump_state (update)")
                    self.jump_state = JumpState.grounded
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                self.change_y = 0
        # handle debug jump state
        if self.DEBUG_PREV_JUMP_STATE != self.jump_state:
            _debug_log("jump state change " + self.jump_state.name)
            self.DEBUG_PREV_JUMP_STATE = self.jump_state

    def calc_grav(self):
        """Calculate effect of gravity."""
        # but override all this if we're on a platform
        if self.is_on_platform():
            self.change_y = 0
            # if we are crouching on the ground.
            if(self.jump_state == JumpState.crouching or
               self.jump_state == JumpState.jumping):
                if(self.crouching_ticks < pygame.time.get_ticks()):
                    # apply impulse of player jump
                    self.change_y = -100
                    self.jump_state = JumpState.jumping
                    self.rect.y = self.rect.y - 1
            else:
                # if we are not crouching or jumping then
                # we are falling, landing, or grounding
                # _debug_log("set grounded jump_state (calc_grav)")
                self.jump_state = JumpState.grounded
        else:
            if self.change_y <= 0:
                self.change_y += .35
            elif self.change_y > 0:
                self.change_y += .35
                self.jump_state = JumpState.falling
        # calmp the parameters
        self.change_y = min(self.change_y, MAX_BASE_FALL_SPEED)
        self.change_y = max(self.change_y, MAX_BASE_JUMP_SPEED)

    def is_on_platform(self):
        """check whether sprite is on a platform."""
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False)
        self.rect.y -= 2
        return (len(platform_hit_list) > 0 or
                self.rect.bottom >= SCREEN_HEIGHT)

    def jump_pressed(self):
        """Called on the frame when the user presses 'jump' button."""
        _debug_log("jump_pressed")
        if self.jump_state == JumpState.grounded:
            self.jump_state = JumpState.crouching
            self.crouching_ticks = pygame.time.get_ticks() + 50
        else:
            print("no jump")

    def jump_released(self):
        """Called on the frame when the user releases 'jump' button."""
        if self.jump_state == JumpState.crouching:
            self.change_y = 12
            self.jump_state = JumpState.jumping
        if self.change_y < 0:
            self.change_y = 0

    # Player-controlled movement:
    def go_left(self):
        """Called when the user hits the left arrow."""
        self.change_x = -6

    def go_right(self):
        """Called when the user hits the right arrow."""
        self.change_x = 6

    def stop(self):
        """Called when the user lets off the keyboard."""
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    """Platforms are sprites the user can jump off of and land on."""

    def __init__(self, width, height):
        """Construct the platorm with a size and position."""
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Green.value)

        self.rect = self.image.get_rect()


class Level(object):
    """
    This is a generic super-class used to define a level.

    Create a child class for each level with level-specific
    info.
    """

    def __init__(self, player):
        """Construct the platform list, enemy list, and player."""
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everythign on this level
    def update(self):
        """Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """Draw everything on this level."""
        # Draw the background
        screen.fill(Color.Blue.value)
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level


class Level_01(Level):
    """Definition for level 1."""

    def __init__(self, player):
        """Create level 1."""
        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    """Main Loop."""
    pygame.init()
    # set up fonts
    basicFont = pygame.font.SysFont(None, 48)

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer Jumper")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump_pressed()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_UP:
                    player.jump_released()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        # set up the text
        text = basicFont.render(player.jump_state.name, True,
                                Color.White.value, Color.Blue.value)
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        screen.blit(text, textRect)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


def _debug_log(stringToPrint):
    if DEBUG_LOG_ENABLED:
        print(stringToPrint)

# Hard-require Python version 3+
if sys.version_info[0] != 3:
    print("This project requires Python 3")
    exit()
if __name__ == "__main__":
    main()
