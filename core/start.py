import pygame
try:
    from config import SCREEN_HEIGHT, SCREEN_WIDTH
except ImportError:
    from core.config import SCREEN_HEIGHT, SCREEN_WIDTH

from PIL import Image

class GifBackground:
    def __init__(self, gif_path, screen_width, screen_height):
        self.frames, self.frame_durations = self.load_gif(gif_path)
        self.width = screen_width
        self.height = screen_height
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()

    @staticmethod
    def load_gif(file_path):
        """Load GIF frames and their durations."""
        gif = Image.open(file_path)
        frames = []
        frame_durations = []

        try:
            while True:
                frame = gif.copy()
                frame = frame.convert("RGBA")  # Ensure compatibility with Pygame
                frames.append(
                    pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                )
                frame_durations.append(gif.info.get("duration", 100) / 1000)
                gif.seek(len(frames))  # Move to the next frame
        except EOFError:
            pass  # End of GIF

        return frames, frame_durations

    def update_and_draw(self, screen):
        """Update the frame index and draw the current frame on the screen."""
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_frame_time

        # Update frame index based on duration
        if elapsed_time >= self.frame_durations[self.frame_index] * 1000:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_frame_time = current_time

        # Draw the current frame
        screen.blit(
            pygame.transform.scale(self.frames[self.frame_index], (self.width, self.height)),
            (0, 0),
        )


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GIF Background Example")

    # Create GifBackground instance by passing the gif path
    gif_path = "assets/tenor.gif"  # Ensure this path is correct
    gif_bg = GifBackground(gif_path, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill((0, 0, 0))

        # Update and draw the GIF
        gif_bg.update_and_draw(screen)

        # Update the display
        pygame.display.flip()

        # Frame rate limit
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
