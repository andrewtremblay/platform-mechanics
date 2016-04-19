import pygame

from base.color import Color


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
