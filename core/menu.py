import pygame
import pygame_gui
import sys
try:
    from core.config import screen, clock, WHITE, BLACK, BLUE, RED, font, small_font, background
except ImportError:
    from config import screen, clock, WHITE, BLACK, BLUE, RED, font, small_font, background, SCREEN_HEIGHT, SCREEN_WIDTH

class Menu:
    def __init__(self):
        self.manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() // 4 - 50), (200, 50)),
            text='INTERSTELLAR',
            manager=self.manager
        )
        self.buttons = [
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() // 2 + i * 60), (200, 50)),
                text=option,
                manager=self.manager
            ) for i, option in enumerate(["Play", "Controls", "Credits", "Exit"])
        ]
    def run(self):
        while True:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.buttons[0]:  # Play
                            try:
                                from core.game import Game
                            except ImportError:
                                from game import Game
                            import json
                            with open('core/hp.json', 'r') as f:
                                data = json.load(f)
                            Game(data['hp']).run()  # Start the game
                        elif event.ui_element == self.buttons[1]:  # Controls
                            self.show_controls()
                        elif event.ui_element == self.buttons[2]:  # Credits
                            self.show_credits()
                        elif event.ui_element == self.buttons[3]:  # Exit
                            pygame.quit()
                            sys.exit()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            static_bg = pygame.transform.scale(background, (1920, 1080))
            screen.blit(static_bg)
            self.manager.draw_ui(screen)
            pygame.display.flip()

    def show_controls(self):
        self._show_screen("Controls", [
            "Use Arrow Keys to Move the Ship.",
            "Game Kraken.",
            "Press Space to Shoot.",
            "Avoid Boss Bullets and Destroy the Boss!",
            "Game Caturn",
            "Click on arrow keys when you see the note!"
        ])

    def show_credits(self):
        self._show_screen("Credits", ["Developed by Samrudh and Vince!"])

    def _show_screen(self, title, lines):
        manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
        title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() // 4 - 50), (200, 50)),
            text=title,
            manager=manager
        )
        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() - 100), (200, 50)),
            text='Back',
            manager=manager
        )
        line_labels = [
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((screen.get_width() // 2 - 150, screen.get_height() // 2 + i * 60), (300, 50)),
                text=line,
                manager=manager
            ) for i, line in enumerate(lines)
        ]

        while True:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == back_button:
                            return

                manager.process_events(event)

            manager.update(time_delta)
            screen.fill(BLACK)
            manager.draw_ui(screen)
            pygame.display.flip()


if __name__ == "__main__":
    Menu().run()