import pygame
import os

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Function to create a better player bullet
def create_player_bullet(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw bullet with a bright blue color and white core
    pygame.draw.rect(surface, CYAN, (0, 0, width, height))
    pygame.draw.rect(surface, WHITE, (width//4, 0, width//2, height))
    
    # Add a glow effect
    pygame.draw.rect(surface, CYAN, (0, 0, width, height), 1)
    
    return surface

# Function to create a better enemy bullet
def create_enemy_bullet(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw bullet with a bright red color and yellow core
    pygame.draw.rect(surface, RED, (0, 0, width, height))
    pygame.draw.rect(surface, YELLOW, (width//4, 0, width//2, height))
    
    # Add a glow effect
    pygame.draw.rect(surface, RED, (0, 0, width, height), 1)
    
    return surface

# Create larger, more visible bullets
player_bullet = create_player_bullet(8, 20)
pygame.image.save(player_bullet, 'assets/bullet.png')
print("Created new bullet.png")

enemy_bullet = create_enemy_bullet(8, 20)
pygame.image.save(enemy_bullet, 'assets/enemy_bullet.png')
print("Created new enemy_bullet.png")

print("New bullet assets created successfully!")
