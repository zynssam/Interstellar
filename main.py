from core.menu import Menu
import pygame
import sys

if __name__ == "__main__":

    # Initialize Pygame
    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Start menu
    Menu().run()  # Open the menu directly

    # Main loop (Menu running inside it)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Update the display
        pygame.display.flip()

        # Frame rate limit
        clock.tick(60)
