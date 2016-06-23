"""A more sophisticated address of a controllers button state.

Not only is it important to keep track of the moments that keys are
 pressed and released, we must also monitor:
  Current pressed button data:
   * How long the button has been pressed.
   * Which buttons are pressed simultaneously.
  Past pressed button data:
   * How long since a button was last pressed.
   * Button press patterns in a given timespan.

  In addition to buttons consider also joysticks,
   but do not prioritize them.
"""
import pygame


class CONTROLS:
    """Represents the sprite that the player controls."""

    def update_player_from_events(self, the_player):
        """Update the internal control scheme from the controls."""
        done = False
        for event in pygame.event.get():
            done = (event.type == pygame.QUIT)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    the_player.go_left()
                if event.key == pygame.K_RIGHT:
                    the_player.go_right()
                if event.key == pygame.K_UP:
                    the_player.jump_pressed()
                # check for escape keys
                if event.key == pygame.K_ESCAPE or \
                        event.key == pygame.K_q or \
                        event.key == pygame.K_DELETE:
                    done = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and the_player.change_x < 0:
                    the_player.stop()
                if event.key == pygame.K_RIGHT and the_player.change_x > 0:
                    the_player.stop()
                if event.key == pygame.K_UP:
                    the_player.jump_released()
        return done

# apply to a global
Controls = CONTROLS()
