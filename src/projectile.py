import pygame

class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 10
        self.sprite = pygame.image.load("assets/sprites/projectile.ppm").convert()
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
