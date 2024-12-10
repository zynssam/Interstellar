import pygame

try:
    from core.config import SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Ship:
    def __init__(self):
        self.image = pygame.image.load('assets/Ship-lev-1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        self.bullets = []  # List to store active bullets
        self.bullet_speed = -10  # Negative for upward movement
        self.bullet_cooldown = 300  # Cooldown in milliseconds
        self.last_shot = 0  # Track the last shot time
        self.health = 100

    def draw(self, surface):
        # Draw the ship
        surface.blit(self.image, self.rect)
        # Draw all bullets
        for bullet in self.bullets:
            pygame.draw.rect(surface, (255, 255, 0), bullet)

    def move(self, keys, camera_offset, corner_margin):
        if keys[pygame.K_UP]:
            if self.rect.top > corner_margin:
                self.rect.y -= self.speed
            else:
                camera_offset[1] += self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < SCREEN_HEIGHT - corner_margin:
                self.rect.y += self.speed
            else:
                camera_offset[1] -= self.speed
        if keys[pygame.K_LEFT]:
            if self.rect.left > corner_margin:
                self.rect.x -= self.speed
            else:
                camera_offset[0] += self.speed
        if keys[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH - corner_margin:
                self.rect.x += self.speed
            else:
                camera_offset[0] -= self.speed

    def shoot(self):
        # Limit shooting to the cooldown period
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.bullet_cooldown:
            bullet = pygame.Rect(self.rect.centerx - 5, self.rect.top - 10, 10, 20)
            self.bullets.append(bullet)
            self.last_shot = current_time

    def update_bullets(self):
        # Move bullets upward and remove those off-screen
        for bullet in self.bullets[:]:
            bullet.y += self.bullet_speed
            if bullet.bottom < 0:
                self.bullets.remove(bullet)
