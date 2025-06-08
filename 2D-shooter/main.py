import pygame
import random
import math
import os
from pygame import mixer

# Initialize pygame
pygame.init()

# Create game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game variables
score = 0
game_over = False
paused = False
level = 1
lives = 3
show_splash = True  # New variable to control splash screen

# Load images
def load_image(name, scale=1):
    try:
        img = pygame.image.load(os.path.join('assets', name)).convert_alpha()
        return pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    except:
        print(f"Error loading image: {name}")
        # Return a colored rectangle as placeholder
        surf = pygame.Surface((50, 50))
        surf.fill(RED)
        return surf

# Load sounds
def load_sound(name):
    try:
        return mixer.Sound(os.path.join('assets', name))
    except:
        print(f"Error loading sound: {name}")
        return None

# Initialize sounds
mixer.init()
try:
    mixer.music.load(os.path.join('assets', 'background.wav'))
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)  # -1 means loop indefinitely
except:
    print("Error loading background music")

# Sound effects
shoot_sound = load_sound('laser.wav')
explosion_sound = load_sound('explosion.wav')
powerup_sound = load_sound('powerup.wav')

# Font
font = pygame.font.SysFont('Arial', 25)
large_font = pygame.font.SysFont('Arial', 40)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('player.png', 0.1)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = 0
        self.power_level = 1
        self.power_timer = 0
        
    def update(self):
        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10
            
        # Power timeout
        if self.power_level > 1 and pygame.time.get_ticks() - self.power_timer > 5000:
            self.power_level -= 1
            self.power_timer = pygame.time.get_ticks()
            
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                if shoot_sound:
                    shoot_sound.play()
            elif self.power_level >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                if shoot_sound:
                    shoot_sound.play()
                    
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        
    def powerup(self):
        self.power_level += 1
        self.power_timer = pygame.time.get_ticks()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('enemy.png', 0.1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.shoot_delay = random.randrange(1000, 3000)
        self.last_shot = pygame.time.get_ticks()
        # Add radius attribute for collision detection
        self.radius = int(self.rect.width * 0.85 / 2)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # If enemy goes off screen, respawn
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            
        # Enemy shooting
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Use scale factor 1.0 instead of 0.1 to make bullets more visible
        self.image = load_image('bullet.png', 1.0)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # Kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Enemy Bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Use scale factor 1.0 instead of 0.1 to make bullets more visible
        self.image = load_image('enemy_bullet.png', 1.0)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 7
        
    def update(self):
        self.rect.y += self.speedy
        # Kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = load_image('explosion1.png', size)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 9:  # Assuming 9 frames of explosion
                self.kill()
            else:
                center = self.rect.center
                self.image = load_image(f'explosion{self.frame}.png', self.size)
                self.rect = self.image.get_rect()
                self.rect.center = center

# Power-up class
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['shield', 'gun'])
        self.image = load_image(f'powerup_{self.type}.png', 0.1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 5
        
    def update(self):
        self.rect.y += self.speedy
        # Kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Function to draw text
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Function to draw text with shadow for better visibility
def draw_text_with_shadow(surf, text, size, x, y, color=WHITE, shadow_color=BLACK):
    # Draw shadow
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, shadow_color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x + 2, y + 2)  # Offset for shadow
    surf.blit(text_surface, text_rect)
    
    # Draw text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
# Function to draw the splash screen
def draw_splash_screen(screen):
    try:
        # Load splash background and logo
        splash_bg = load_image('splash_bg.png', 1.0)
        splash_logo = load_image('splash_logo.png', 1.0)
        
        # Draw background
        screen.blit(splash_bg, (0, 0))
        
        # Draw logo
        logo_rect = splash_logo.get_rect()
        logo_rect.center = (WIDTH // 2, HEIGHT // 3)
        screen.blit(splash_logo, logo_rect)
        
        # Draw game title
        draw_text_with_shadow(screen, "SPACE SHOOTER", 64, WIDTH // 2, HEIGHT // 2, BLUE)
        
        # Draw instructions
        draw_text_with_shadow(screen, "Arrow Keys: Move", 22, WIDTH // 2, HEIGHT * 2 // 3)
        draw_text_with_shadow(screen, "Space: Shoot", 22, WIDTH // 2, HEIGHT * 2 // 3 + 30)
        draw_text_with_shadow(screen, "P: Pause", 22, WIDTH // 2, HEIGHT * 2 // 3 + 60)
        
        # Draw start prompt
        draw_text_with_shadow(screen, "Press ENTER to start", 28, WIDTH // 2, HEIGHT * 5 // 6, GREEN)
        
        # Draw version and credits
        draw_text_with_shadow(screen, "v1.0", 16, WIDTH - 50, HEIGHT - 30)
        draw_text_with_shadow(screen, "© 2025 Space Games", 16, WIDTH // 2, HEIGHT - 30)
        
    except Exception as e:
        # Fallback if images can't be loaded
        screen.fill(BLACK)
        
        # Draw stars
        for i in range(100):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            pygame.draw.circle(screen, WHITE, (x, y), 1)
        
        # Draw title and instructions
        draw_text_with_shadow(screen, "SPACE SHOOTER", 64, WIDTH // 2, HEIGHT // 3, BLUE)
        draw_text_with_shadow(screen, "Arrow Keys: Move", 22, WIDTH // 2, HEIGHT // 2)
        draw_text_with_shadow(screen, "Space: Shoot", 22, WIDTH // 2, HEIGHT // 2 + 30)
        draw_text_with_shadow(screen, "P: Pause", 22, WIDTH // 2, HEIGHT // 2 + 60)
        draw_text_with_shadow(screen, "Press ENTER to start", 28, WIDTH // 2, HEIGHT * 3 // 4, GREEN)

# Function to draw shield bar
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Function to draw lives
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# Function to spawn a new enemy
def spawn_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Function to spawn a new powerup
def spawn_powerup():
    if random.random() > 0.95:  # 5% chance
        powerup = Powerup()
        all_sprites.add(powerup)
        powerups.add(powerup)

# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)
    
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if paused:
                    running = False
                else:
                    paused = True
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                score = 0
                level = 1
                player = Player()
                all_sprites = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                enemy_bullets = pygame.sprite.Group()
                powerups = pygame.sprite.Group()
                all_sprites.add(player)
                for i in range(8):
                    spawn_enemy()
            # Handle splash screen
            if event.key == pygame.K_RETURN and show_splash:
                show_splash = False
    
    # Show splash screen if needed
    if show_splash:
        draw_splash_screen(screen)
        pygame.display.flip()
        continue
    
    if paused or game_over:
        # Draw / render
        screen.fill(BLACK)
        
        # Draw stars (background)
        for i in range(100):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            pygame.draw.circle(screen, WHITE, (x, y), 1)
        
        all_sprites.draw(screen)
        
        # Draw UI
        draw_text(screen, f"Score: {score}", 25, WIDTH / 2, 10)
        draw_text(screen, f"Level: {level}", 25, WIDTH / 2, 40)
        draw_shield_bar(screen, 5, 5, player.shield)
        
        # Draw lives
        mini_player_img = pygame.transform.scale(player.image, (25, 19))
        draw_lives(screen, WIDTH - 100, 5, player.lives, mini_player_img)
        
        # Draw game over screen
        if game_over:
            # Add semi-transparent overlay
            game_over_overlay = pygame.Surface((WIDTH, HEIGHT))
            game_over_overlay.set_alpha(180)
            game_over_overlay.fill(BLACK)
            screen.blit(game_over_overlay, (0, 0))
            
            draw_text_with_shadow(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
            draw_text_with_shadow(screen, f"Final Score: {score}", 36, WIDTH / 2, HEIGHT / 2)
            draw_text_with_shadow(screen, "Press R to restart", 22, WIDTH / 2, HEIGHT * 3/4)
        
        # Draw pause screen
        if paused:
            # Add semi-transparent overlay
            pause_overlay = pygame.Surface((WIDTH, HEIGHT))
            pause_overlay.set_alpha(180)
            pause_overlay.fill(BLACK)
            screen.blit(pause_overlay, (0, 0))
            
            # Draw pause text
            draw_text_with_shadow(screen, "PAUSED", 64, WIDTH / 2, HEIGHT / 4, WHITE)
            draw_text_with_shadow(screen, "Press P to continue", 28, WIDTH / 2, HEIGHT / 2)
            draw_text_with_shadow(screen, "Press ESC to quit", 22, WIDTH / 2, HEIGHT / 2 + 40)
            
            # Draw current score and level
            draw_text_with_shadow(screen, f"Score: {score}", 26, WIDTH / 2, HEIGHT * 3/4)
            draw_text_with_shadow(screen, f"Level: {level}", 26, WIDTH / 2, HEIGHT * 3/4 + 40)
        
        # Flip the display
        pygame.display.flip()
        continue
    
    # Update
    all_sprites.update()
    
    # Check if bullets hit enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        # Use a fixed score value instead of relying on radius attribute
        score += 50
        if explosion_sound:
            explosion_sound.play()
        explosion = Explosion(hit.rect.center, 0.5)
        all_sprites.add(explosion)
        spawn_enemy()
        spawn_powerup()
    
    # Check if enemy bullets hit player
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.shield -= 10
        if player.shield <= 0:
            if explosion_sound:
                explosion_sound.play()
            death_explosion = Explosion(player.rect.center, 1)
            all_sprites.add(death_explosion)
            player.lives -= 1
            player.shield = 100
            player.hide()
            
            if player.lives == 0:
                game_over = True
    
    # Check if player collides with enemies
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.shield -= 20
        if explosion_sound:
            explosion_sound.play()
        explosion = Explosion(hit.rect.center, 0.5)
        all_sprites.add(explosion)
        spawn_enemy()
        
        if player.shield <= 0:
            if explosion_sound:
                explosion_sound.play()
            death_explosion = Explosion(player.rect.center, 1)
            all_sprites.add(death_explosion)
            player.lives -= 1
            player.shield = 100
            player.hide()
            
            if player.lives == 0:
                game_over = True
    
    # Check if player got powerups
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield > 100:
                player.shield = 100
            if powerup_sound:
                powerup_sound.play()
        if hit.type == 'gun':
            player.powerup()
            if powerup_sound:
                powerup_sound.play()
    
    # Shooting
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.shoot()
    
    # Level up
    if len(enemies) < 5:
        for i in range(5):
            spawn_enemy()
        level += 1
    
    # Draw / render
    screen.fill(BLACK)
    
    # Draw stars (background)
    for i in range(100):
        x = random.randrange(0, WIDTH)
        y = random.randrange(0, HEIGHT)
        pygame.draw.circle(screen, WHITE, (x, y), 1)
    
    all_sprites.draw(screen)
    
    # Draw UI
    draw_text(screen, f"Score: {score}", 25, WIDTH / 2, 10)
    draw_text(screen, f"Level: {level}", 25, WIDTH / 2, 40)
    draw_shield_bar(screen, 5, 5, player.shield)
    
    # Draw lives
    mini_player_img = pygame.transform.scale(player.image, (25, 19))
    draw_lives(screen, WIDTH - 100, 5, player.lives, mini_player_img)
    
    # Draw game over screen
    if game_over:
        # Add semi-transparent overlay
        game_over_overlay = pygame.Surface((WIDTH, HEIGHT))
        game_over_overlay.set_alpha(180)
        game_over_overlay.fill(BLACK)
        screen.blit(game_over_overlay, (0, 0))
        
        draw_text_with_shadow(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
        draw_text_with_shadow(screen, f"Final Score: {score}", 36, WIDTH / 2, HEIGHT / 2)
        draw_text_with_shadow(screen, "Press R to restart", 22, WIDTH / 2, HEIGHT * 3/4)
    
    # Draw pause screen
    if paused:
        # Add semi-transparent overlay
        pause_overlay = pygame.Surface((WIDTH, HEIGHT))
        pause_overlay.set_alpha(180)
        pause_overlay.fill(BLACK)
        screen.blit(pause_overlay, (0, 0))
        
        # Draw pause text
        draw_text_with_shadow(screen, "PAUSED", 64, WIDTH / 2, HEIGHT / 4, WHITE)
        draw_text_with_shadow(screen, "Press P to continue", 28, WIDTH / 2, HEIGHT / 2)
        draw_text_with_shadow(screen, "Press ESC to quit", 22, WIDTH / 2, HEIGHT / 2 + 40)
        
        # Draw current score and level
        draw_text_with_shadow(screen, f"Score: {score}", 26, WIDTH / 2, HEIGHT * 3/4)
        draw_text_with_shadow(screen, f"Level: {level}", 26, WIDTH / 2, HEIGHT * 3/4 + 40)
    
    # Flip the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
