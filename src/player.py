import pygame
from projectile import Projectile

class Player:
    def __init__(self, character):
        self.character = character
        self.health = self.character.stats["health"]
        self.x = 400
        self.y = 300
        self.speed = 5

        # Animation attributes
        self.sprites = [
            pygame.image.load(self.character.sprite).convert(),
            pygame.image.load(self.character.sprite_walk).convert()
        ]
        self.current_sprite_index = 0
        self.image = self.sprites[self.current_sprite_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.is_moving = False
        self.animation_timer = 0
        self.animation_speed = 10 # lower is faster

    def handle_events(self, events):
        new_projectiles = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Shoot a projectile to the right
                    new_projectiles.append(Projectile(self.x, self.y, 1, 0))
        return new_projectiles

    def update(self):
        self.is_moving = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.is_moving = True

        self.rect.center = (self.x, self.y)

        # Animation logic
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)
                self.image = self.sprites[self.current_sprite_index]
        else:
            self.current_sprite_index = 0
            self.image = self.sprites[self.current_sprite_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
