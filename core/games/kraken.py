import pygame
import random
import sys
try:
    from core.ship import Ship
    from core.config import RED, YELLOW, SCREEN_HEIGHT, SCREEN_WIDTH,screen,clock, BLACK
    from core.menu import Menu
except ImportError:
    from ship import Ship
    from config import RED, YELLOW, SCREEN_HEIGHT, SCREEN_WIDTH,screen,clock, BLACK
    from menu import Menu
class FinalBoss:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/kraken.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 300
        self.speed = 3
        self.bullets = []
        self.bullet_cooldown = 1000
        self.last_shot = 0

    def move(self):
        self.rect.x += self.speed
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.speed = -self.speed

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.bullet_cooldown:
            bullet = pygame.Rect(self.rect.centerx - 10, self.rect.bottom, 20, 20)
            self.bullets.append(bullet)
            self.last_shot = current_time

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.y += 5
            if bullet.top > SCREEN_HEIGHT:
                self.bullets.remove(bullet)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(surface, RED, bullet)
        # Draw health bar
        pygame.draw.rect(surface, RED, (SCREEN_WIDTH - 210, 10, 200, 10))  # Health bar background
        pygame.draw.rect(surface, YELLOW, (SCREEN_WIDTH - 210, 10, 200 * (self.health / 300), 10)) 


import pygame
import pygame_gui
import random
from core.ship import Ship  
from core.config import RED, YELLOW, SCREEN_HEIGHT, SCREEN_WIDTH, screen, clock, BLACK, background

# FinalBoss class as defined earlier (not included here for brevity)
kraken_complete = False
def main():
    # Initialize pygame_gui
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Create Game Over Panel (hidden by default)
    game_over_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100), (300, 200)),
        manager=manager,
    object_id="#game_over_panel"
    )
    game_over_panel.hide()

    # Add a label to display the result message
    result_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((25, 60), (250, 40)),
        text="",
        manager=manager,
        container=game_over_panel,
        object_id="#result_label"
    )

        # Add a Restart button (initially hidden)
    restart_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((75, 120), (150, 40)),
        text="Restart",
        manager=manager,
        container=game_over_panel,
        object_id="#restart_button"
    )
    restart_button.hide()  # Hide restart button by default

        # Initialize game objects
    ship = Ship()
    boss = FinalBoss(SCREEN_WIDTH // 2, 50)

        # Game state variables
    running = True
    game_over = False

    while running:
        time_delta = clock.tick(60) / 1000.0
        static_bg = pygame.transform.scale(background, (1920, 1080))
        screen.blit(static_bg)
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Menu().run()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == restart_button:
                        # Restart game logic (only if lost)
                        if ship.health <= 0:
                            ship.health = 100
                            boss.health = 300
                            game_over = False
                            game_over_panel.hide()
                            restart_button.hide()  # Hide restart button again
            manager.process_events(event)

        if not game_over:
            # Ship logic
            ship.move(keys, [0, 0], 100)
            if keys[pygame.K_SPACE]:
                ship.shoot()
            ship.update_bullets()

            # Boss logic
            boss.move()
            boss.attack()
            boss.update_bullets()

            # Check collisions (Ship bullets -> Boss)
            for bullet in ship.bullets[:]:
                if boss.rect.colliderect(bullet):
                    boss.health -= 10
                    ship.bullets.remove(bullet)

            # Check collisions (Boss bullets -> Ship)
            for bullet in boss.bullets[:]:
                if ship.rect.colliderect(bullet):
                    ship.health -= 10
                    boss.bullets.remove(bullet)

            # End game conditions
            if boss.health <= 0:
                result_label.set_text("You Won!")
                game_over_panel.show()
                game_over = True
                restart_button.hide()  # Hide restart button on win

                # Update the display to show the "You Won!" message
                manager.update(time_delta)
                manager.draw_ui(screen)
                pygame.display.flip()

                # Wait for a second
                pygame.time.wait(1000)

                Menu().run()

            if ship.health <= 0:
                result_label.set_text("You Were Defeated!")
                game_over_panel.show()
                game_over = True
                restart_button.show() # Show restart button only on loss 

            # Draw everything
        ship.draw(screen)
        boss.draw(screen)

        # Draw Player Health Bar
        pygame.draw.rect(screen, RED, (10, SCREEN_HEIGHT - 30, 200, 10))  # Background
        pygame.draw.rect(screen, YELLOW, (10, SCREEN_HEIGHT - 30, 200 * (ship.health / 100), 10))  # Foreground

        # Update GUI
        manager.update(time_delta)
        manager.draw_ui(screen)

        # Update display
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__" :
    main()