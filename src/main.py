"""main.py initializes pygame and controls the main game loop."""
import sys
import pygame
from base.color import Color
import configs as conf
import levels as lvls
from sprites import player

# PYTHON 3+ ONLY BEYOND THIS POINT
if sys.version_info[0] != 3:
    print("This project requires Python 3")
    exit()


def main():
    """control the initialization of levels and mechanics."""
    pygame.init()
    # start loading the relevant data
    # set up fonts
    basicFont = pygame.font.SysFont(None, 48)
    # Set the height and width of the screen
    size = [conf.UI.SCREEN_WIDTH, conf.UI.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer Jumper")

    # Create the player
    the_player = player.Player()

    # Create all the levels
    level_list = lvls.build_levels(the_player)

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    the_player.level = current_level

    the_player.rect.x = 340
    the_player.rect.y = conf.UI.SCREEN_HEIGHT - the_player.rect.height
    active_sprite_list.add(the_player)

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
                    the_player.go_left()
                if event.key == pygame.K_RIGHT:
                    the_player.go_right()
                if event.key == pygame.K_UP:
                    the_player.jump_pressed()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and the_player.change_x < 0:
                    the_player.stop()
                if event.key == pygame.K_RIGHT and the_player.change_x > 0:
                    the_player.stop()
                if event.key == pygame.K_UP:
                    the_player.jump_released()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if the_player.rect.right > conf.UI.SCREEN_WIDTH:
            the_player.rect.right = conf.UI.SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if the_player.rect.left < 0:
            the_player.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        # set up the text
        text = basicFont.render(the_player.jump_state.name, True,
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

if __name__ == "__main__":
    main()
