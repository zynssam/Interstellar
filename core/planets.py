import pygame
import math
import sys
try:
    from core.menu import Menu
    from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
    from core.lonlinessbar import HealthBar
except ImportError:
    from menu import Menu 
    from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

planet_png = 'assets/planet.png'
class Planets:
    def __init__(self, screen, camera_offset):
        self.screen = screen
        self.camera_offset = camera_offset
        self.circle_radius = 600
        self.circle_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)

        # Load planet images (reduced to three)
        self.planets_images = [
            pygame.transform.scale(pygame.image.load('assets/catplanet.png'), (100, 100)),
            pygame.transform.scale(pygame.image.load(planet_png), (100, 100)),
            pygame.transform.scale(pygame.image.load('assets/kraken.png'), (100, 100)),
        ]

        # Planet positions (reduced to three)
        self.planet_positions = [
            (
                self.circle_center[0] + math.cos(math.radians(angle)) * self.circle_radius,
                self.circle_center[1] + math.sin(math.radians(angle)) * self.circle_radius,
            )
            for angle in range(205, 300, 45)  # Reduced range
        ]

        # Map planet behaviors (reduced to three)
        self.planet_behaviors = [
            self.land_on_planet1,
            self.land_on_planet2,
            self.land_on_planet3,
        ]

    def draw(self):
        for i, pos in enumerate(self.planet_positions):
            adjusted_pos = (pos[0] + self.camera_offset[0], pos[1] + self.camera_offset[1])
            self.screen.blit(self.planets_images[i], (int(adjusted_pos[0] - 50), int(adjusted_pos[1] - 50)))

    def check_collision(self, ship):
        """
        Check if the ship collides with any planet.
        :param ship: The player's ship object.
        :return: (bool, int) - Whether a collision occurred, and the planet index (if any).
        """
        for i, pos in enumerate(self.planet_positions):
            adjusted_pos = (pos[0] + self.camera_offset[0], pos[1] + self.camera_offset[1])
            distance = math.sqrt(
                (ship.rect.centerx - adjusted_pos[0]) ** 2
                + (ship.rect.centery - adjusted_pos[1]) ** 2
            )
            if distance < 75:  # Close enough to a planet
                return True, i  # Collision detected
        return False, -1  # No collision detected

    def handle_collision(self, planet_index):
        """
        Handle collision by triggering the specific behavior for the landed planet.
        :param planet_index: The index of the collided planet.
        """
        if 0 <= planet_index < len(self.planet_behaviors):
            self.planet_behaviors[planet_index]()

    # Specific behaviors for each planet (reduced to three)
    def land_on_planet1(self):
        try:
            from core.games.caturn import main
        except ImportError:
            from games.caturn import main
        main()

    def land_on_planet2(self):
        self.display_message("You Found A Survivor!!!!")
        HealthBar(50, 50, 400, 40, 100).current_hp = 100
        import time
        time.sleep(5)  # Wait for 5 seconds
    
    # Add code to open the menu here
    # Assuming Menu is the class you're trying to open
        from core.menu import Menu
        Menu().run()

    def land_on_planet3(self):
        try:
            from core.games.kraken import main
        except ImportError:
            from games.kraken import main
        main()

    def display_message(self, message):
        """
        Displays a temporary message on the screen.
        :param message: The message to display.
        """
        font = pygame.font.Font(None, 60)
        rendered_message = font.render(message, True, WHITE)
        message_rect = rendered_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.fill(BLACK)
        self.screen.blit(rendered_message, message_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Display the message for 2 seconds
