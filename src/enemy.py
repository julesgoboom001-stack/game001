import pygame
import math

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.speed = 2
        self.sprite = pygame.image.load("assets/sprites/enemy.ppm").convert()
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

    def update(self, player):
        # Move towards the player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.x += dx * self.speed
            self.y += dy * self.speed

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
