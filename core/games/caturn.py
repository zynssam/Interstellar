import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
import os

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

try:
    from core.menu import Menu
    from core.config import BLACK, RED, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH, background
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Improved Mini Rhythm Game")

# Font setup
font = pygame.font.Font(None, 36)

# Game variables
clock = pygame.time.Clock()
FPS = 60
score = 0
misses = 0

# Load assets
try:
    pygame.mixer.music.load("assets/meow.mp3")  # Replace with your song file
    note_image = pygame.image.load("assets/arrows.png")  # Replace with your note image
    note_image = pygame.transform.scale(note_image, (50, 50))
    background = pygame.image.load("assets/bg.png")  # Load background image
except FileNotFoundError as e:
    print(f"Error loading assets: {e}")
    sys.exit(1)

# Note class
class Note:
    def __init__(self, x, key):
        self.x = x
        self.y = -50  # Start above the screen
        self.key = key
        self.speed = 5
        self.hit = False

    def move(self):
        if not self.hit:
            self.y += self.speed

    def draw(self):
        if not self.hit:
            screen.blit(note_image, (self.x, self.y))

    def is_in_target(self, target_y):
        """Check if the note is in the hit zone."""
        return target_y - 30 < self.y < target_y + 30

# Create initial notes
lanes = {
    pygame.K_LEFT: (150, "LEFT"),
    pygame.K_DOWN: (300, "DOWN"),
    pygame.K_UP: (450, "UP"),
    pygame.K_RIGHT: (600, "RIGHT"),
}
notes = []

def spawn_note():
    """Spawns a new note in a random lane."""
    key = random.choice(list(lanes.keys()))
    x, _ = lanes[key]
    notes.append(Note(x, key))

def display_message(message, options=None):
    """Displays a message in the center of the screen."""
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    if options:
        for i, option in enumerate(options):
            option_text = font.render(option, True, WHITE)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50 + i * 40))
            screen.blit(option_text, option_rect)

    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds if no options are shown

def game_over():
    """Displays Game Over screen and options to play again or quit."""
    global score, misses
    options = ["Press R to Restart", "Press M to Go to Menu"]
    display_message("Game Over!", options)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    score = 0
                    misses = 0
                    return  # Exit the loop and restart the game
                elif event.key == pygame.K_m:  # Go to Menu
                    Menu().run()  # Go to the menu

# Main game loop
def main():
    global score, misses
    running = True
    pygame.mixer.music.play(-1)  # Loop the song indefinitely
    static_bg = pygame.transform.scale(background, (1920, 1080))
    
    # Target line position
    target_y = SCREEN_HEIGHT - 100
    spawn_timer = 0

    while running:
        screen.blit(static_bg, (0, 0))  # Draw background every frame

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    Menu().run()

        # Draw target line
        pygame.draw.line(screen, WHITE, (0, target_y), (SCREEN_WIDTH, target_y), 5)

        # Draw score and misses
        score_text = font.render(f"Score: {score}", True, WHITE)
        misses_text = font.render(f"Misses: {misses}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(misses_text, (10, 60))

        # Draw key lane labels
        for key, (x, label) in lanes.items():
            label_text = font.render(label, True, RED)
            text_rect = label_text.get_rect(center=(x + 25, SCREEN_HEIGHT - 50))
            screen.blit(label_text, text_rect)

        # Handle note movement and input
        keys = pygame.key.get_pressed()
        for note in notes[:]:
            note.move()
            note.draw()

            if note.is_in_target(target_y) and keys[note.key]:
                notes.remove(note)
                score += 10
                break

            if note.y > SCREEN_HEIGHT:
                notes.remove(note)
                misses += 1

        # Check win/lose conditions
        if score >= 200:
            display_message("You Win!")
            tk.Tk().withdraw()
            messagebox.showinfo("Congratulations!", "You won!")
            running = False
            Menu().run()

        elif misses >= 5:
            game_over()

        # Spawn new notes periodically
        spawn_timer += 1
        if spawn_timer >= FPS:  # Spawn a note every second
            spawn_note()
            spawn_timer = 0

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
