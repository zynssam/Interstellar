import pygame
import sys
try:
    from core.config import screen, clock, BLACK, background
    from core.ship import Ship
    from core.lonlinessbar import HealthBar
    from core.planets import Planets
except ImportError:
    from config import screen, clock, BLACK
    from ship import Ship 
    from lonlinessbar import HealthBar
    from planets import Planets

survivorstatus = False
class Game:
    def __init__(self, hp=100):
        self.ship = Ship()
        self.health_bar = HealthBar(50, 50, 400, 40, 100)
        self.health_bar.hp = hp
        self.camera_offset = [0, 0]
        self.planets = Planets(screen, self.camera_offset)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.health_bar.write_data(self.health_bar.hp)
                    try:
                        from core.menu import Menu
                    except ImportError:
                        from menu import Menu
                    Menu().run()

            # Update ship movement
            static_bg = pygame.transform.scale(background, (1920, 1080))
            screen.blit(static_bg)
            keys = pygame.key.get_pressed()
            self.ship.move(keys, self.camera_offset, 100)

            # Check collision with planets
            collision, planet_index = self.planets.check_collision(self.ship)
            if collision:
                self.planets.handle_collision(planet_index)

            # Draw game elements
            self.health_bar.draw(screen)
            self.health_bar.update(1)
            self.planets.draw()
            self.ship.draw(screen)

            # Update display and regulate FPS
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()