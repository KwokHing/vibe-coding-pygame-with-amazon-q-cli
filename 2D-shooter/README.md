# How to Run the Space Shooter Game

## Prerequisites
- Python 3.x
- Pygame library

## Installation Steps

1. **Install Pygame** (if not already installed):
   ```
   pip3 install pygame
   ```

2. **Run the game**:
   ```
   cd /home/dmin/2D_shooter
   python3 main.py
   ```

## Game Controls
- **Arrow Keys**: Move the player's spaceship
- **Space**: Shoot
- **P**: Pause/Unpause the game
- **R**: Restart after game over
- **ESC**: Quit the game

## About the Assets
The game uses simple programmatically generated assets:

- **Player Ship**: A green triangular ship with blue cockpit and red engines
- **Enemy Ships**: Red triangular ships with red details
- **Bullets**: Blue rectangles for player bullets, red for enemy bullets
- **Power-ups**: 
  - Blue circle with white square (Shield)
  - Yellow circle with red square (Gun upgrade)
- **Explosions**: Animation frames that grow and change color

The sound files are empty placeholders. For a better gaming experience, you can replace them with actual sound effects from free sound libraries like:
- [Freesound](https://freesound.org/)
- [OpenGameArt](https://opengameart.org/)

## Customizing Assets
If you want to use your own custom assets:
1. Create or download your own image and sound files
2. Replace the files in the `assets` directory with your own
3. Make sure to keep the same filenames or update the code to match your new filenames
