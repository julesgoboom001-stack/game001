import pygame
import os

# Define colors and size for the placeholders
COLORS = {
    "warrior": (255, 0, 0),   # Red
    "mage":    (0, 0, 255),   # Blue
    "rogue":   (0, 255, 0),   # Green
}
SIZE = (32, 32)
SPRITES_DIR = "assets/sprites"

def create_placeholder_sprites():
    """Creates placeholder sprite images for each character class."""
    pygame.init()
    os.makedirs(SPRITES_DIR, exist_ok=True)

    for character, color in COLORS.items():
        # Create a 32x32 surface
        sprite = pygame.Surface(SIZE)
        sprite.fill(color)

        # Save the surface as a PNG image
        filepath = os.path.join(SPRITES_DIR, f"{character}.png")
        pygame.image.save(sprite, filepath)
        print(f"Created placeholder sprite: {filepath}")

if __name__ == "__main__":
    create_placeholder_sprites()
