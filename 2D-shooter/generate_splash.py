import pygame
import os

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Function to create a splash logo
def create_splash_logo(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw space background
    surface.fill(BLACK)
    
    # Draw some stars
    for i in range(50):
        x = pygame.math.Vector2(pygame.math.Vector2(1, 0).rotate(i * 7.2))
        pygame.draw.circle(surface, WHITE, 
                          (int(width/2 + x.x * (i % 5) * 20), 
                           int(height/2 + x.y * (i % 5) * 20)), 
                          1)
    
    # Draw a large spaceship silhouette
    ship_points = [
        (width/2, height/3),
        (width/3, height*2/3),
        (width*2/5, height*2/3),
        (width*2/5, height*4/5),
        (width*3/5, height*4/5),
        (width*3/5, height*2/3),
        (width*2/3, height*2/3)
    ]
    pygame.draw.polygon(surface, BLUE, ship_points)
    
    # Add engine glow
    pygame.draw.rect(surface, RED, (width*2/5, height*4/5, width/10, height/10))
    pygame.draw.rect(surface, RED, (width/2, height*4/5, width/10, height/10))
    
    # Add cockpit
    pygame.draw.ellipse(surface, YELLOW, (width*9/20, height*2/5, width/10, height/10))
    
    return surface

# Create splash background
splash_bg = pygame.Surface((800, 600))
splash_bg.fill(BLACK)

# Add stars to background
for i in range(200):
    x = pygame.math.Vector2(pygame.math.Vector2(1, 0).rotate(i * 1.8))
    radius = 1
    if i % 20 == 0:
        radius = 2
    pygame.draw.circle(splash_bg, WHITE, 
                      (int(400 + x.x * (i % 10) * 40), 
                       int(300 + x.y * (i % 10) * 30)), 
                      radius)

# Save splash background
pygame.image.save(splash_bg, 'assets/splash_bg.png')
print("Created splash_bg.png")

# Create logo
logo = create_splash_logo(400, 300)
pygame.image.save(logo, 'assets/splash_logo.png')
print("Created splash_logo.png")

print("Splash screen assets created successfully!")
