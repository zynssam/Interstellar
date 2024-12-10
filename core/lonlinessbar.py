import time
import pygame
import json
try: 
    from core.config import RED, GREEN
except ImportError:
    from config import RED, GREEN

hp_file = 'core/hp.json'

class HealthBar:
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.last_update = time.time()
        self.font = pygame.font.SysFont(None, 24)  # Initialize font
    
    def current_hp(self):
        return self.hp
    def draw(self, surface):
        # Draw border
        pygame.draw.rect(surface, (0, 0, 0), (self.x - 2, self.y - 2, self.w + 4, self.h + 4), 1)
        
        # Draw background
        pygame.draw.rect(surface, RED, (self.x, self.y, self.w, self.h))
        
        # Draw foreground
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.w * ratio, self.h))
        
        # Render text
        text = self.font.render("Loneliness Bar", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + self.w // 2, self.y - 10))
        surface.blit(text, text_rect)

    def update(self, hp):
        if time.time() - self.last_update >= 5:
            if self.hp > 0:
                self.hp -= hp
            self.last_update = time.time()
    
    def load_hp(self):
        try:
            with open(hp_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle the case where the file is missing or contains invalid JSON
            data = {"hp": 100}  # Default value or structure
            with open(hp_file, 'w') as f:
                json.dump(data, f)
        return data
    
    def write_data(self, hp):
        data = {"hp": hp}
        with open(hp_file, 'w') as f:
            json.dump(data, f)

    
