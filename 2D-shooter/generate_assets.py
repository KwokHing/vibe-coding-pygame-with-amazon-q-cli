import pygame
import os
import math

# Initialize pygame
pygame.init()

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Function to create a simple spaceship
def create_player_ship(width, height, color):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw ship body
    pygame.draw.polygon(surface, color, [(width//2, 0), (0, height), (width, height)])
    
    # Draw cockpit
    pygame.draw.ellipse(surface, BLUE, (width//4, height//2, width//2, height//4))
    
    # Draw engines
    pygame.draw.rect(surface, RED, (width//4, height-height//6, width//8, height//6))
    pygame.draw.rect(surface, RED, (width-width//4-width//8, height-height//6, width//8, height//6))
    
    return surface

# Function to create an enemy ship
def create_enemy_ship(width, height, color):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw ship body
    pygame.draw.polygon(surface, color, [(0, 0), (width, 0), (width//2, height)])
    
    # Draw details
    pygame.draw.ellipse(surface, RED, (width//4, height//4, width//2, height//4))
    
    return surface

# Function to create a bullet
def create_bullet(width, height, color):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw bullet
    pygame.draw.rect(surface, color, (0, 0, width, height))
    
    return surface

# Function to create a power-up
def create_powerup(width, height, color, symbol_color):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw power-up background
    pygame.draw.ellipse(surface, color, (0, 0, width, height))
    
    # Draw symbol
    pygame.draw.rect(surface, symbol_color, (width//4, height//4, width//2, height//2))
    
    return surface

# Function to create explosion frames
def create_explosion_frame(width, height, frame, total_frames):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Calculate size based on frame number
    size_factor = frame / total_frames
    actual_size = int(width * size_factor)
    
    # Mix colors based on frame
    if frame < total_frames // 3:
        color = YELLOW
    elif frame < total_frames * 2 // 3:
        color = RED
    else:
        color = (128, 128, 128)  # Gray smoke
    
    # Draw explosion
    pygame.draw.circle(surface, color, (width//2, height//2), actual_size)
    
    return surface

# Create player ship
player_ship = create_player_ship(100, 80, GREEN)
pygame.image.save(player_ship, 'assets/player.png')
print("Created player.png")

# Create enemy ship
enemy_ship = create_enemy_ship(80, 60, RED)
pygame.image.save(enemy_ship, 'assets/enemy.png')
print("Created enemy.png")

# Create player bullet
player_bullet = create_bullet(10, 30, BLUE)
pygame.image.save(player_bullet, 'assets/bullet.png')
print("Created bullet.png")

# Create enemy bullet
enemy_bullet = create_bullet(8, 20, RED)
pygame.image.save(enemy_bullet, 'assets/enemy_bullet.png')
print("Created enemy_bullet.png")

# Create shield power-up
shield_powerup = create_powerup(40, 40, BLUE, WHITE)
pygame.image.save(shield_powerup, 'assets/powerup_shield.png')
print("Created powerup_shield.png")

# Create gun power-up
gun_powerup = create_powerup(40, 40, YELLOW, RED)
pygame.image.save(gun_powerup, 'assets/powerup_gun.png')
print("Created powerup_gun.png")

# Create explosion frames
total_frames = 9
for i in range(1, total_frames + 1):
    explosion = create_explosion_frame(100, 100, i, total_frames)
    pygame.image.save(explosion, f'assets/explosion{i}.png')
    print(f"Created explosion{i}.png")

print("All image assets created successfully!")

# Now let's create placeholder sound files
# We'll create empty WAV files with the correct names
# In a real game, you would replace these with actual sound effects

def create_empty_wav(filename, duration=1.0, sample_rate=44100):
    """Create an empty WAV file with the given filename."""
    import wave
    import struct
    
    # Create an empty WAV file
    with wave.open(f'assets/{filename}', 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Generate silent audio data
        num_frames = int(duration * sample_rate)
        for _ in range(num_frames):
            wav_file.writeframes(struct.pack('h', 0))
    
    print(f"Created {filename}")

# Create sound placeholders
create_empty_wav('background.wav', duration=5.0)
create_empty_wav('laser.wav', duration=0.5)
create_empty_wav('explosion.wav', duration=1.0)
create_empty_wav('powerup.wav', duration=0.5)

print("All sound assets created successfully!")
print("\nNote: The sound files are empty placeholders. Replace them with real sound effects for a better gaming experience.")
