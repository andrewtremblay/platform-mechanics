"""Platform package."""
import pygame

from base.color import Color


class Platform(pygame.sprite.Sprite):
    """Platforms are sprites the user can jump off of and land on."""

    def __init__(self, width, height):
        """Construct the platorm with a size and position."""
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Green.value)

        self.rect = self.image.get_rect()
