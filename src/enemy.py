import pygame
import math

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.speed = 2
        self.xp_value = 50

        self.sprites = [
            pygame.image.load("assets/sprites/enemy.ppm").convert(),
            pygame.image.load("assets/sprites/enemy_attack.ppm").convert()
        ]
        self.current_sprite_index = 0
        self.image = self.sprites[self.current_sprite_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.attack_range = 50
        self.attack_cooldown = 60 # 1 second cooldown at 60fps
        self.cooldown_timer = 0
        self.is_attacking = False

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            self.is_attacking = False # Not actively attacking during cooldown
            self.current_sprite_index = 0 # Revert to normal sprite

        if dist < self.attack_range:
            if self.cooldown_timer == 0:
                self.is_attacking = True
                self.current_sprite_index = 1 # Show attack sprite
                self.cooldown_timer = self.attack_cooldown
        else:
            # Move towards the player if not in attack range
            if dist > 0:
                dx, dy = dx / dist, dy / dist
                self.x += dx * self.speed
                self.y += dy * self.speed

        self.image = self.sprites[self.current_sprite_index]
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
