import pygame
from projectile import Projectile
import math
from items import all_items
from skills import Skill

class Player:
    def __init__(self, character):
        self.character = character
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

        self.inventory = []
        self.equipment = {}
        self.skills = {
            "mining": Skill(),
            "blacksmithing": Skill(),
        }

        # Equip a sword by default for testing
        self.equipment["weapon"] = all_items["sword"]

        self.recalculate_stats()
        self.health = self.stats["health"]

        self.x = 400
        self.y = 300
        self.speed = 5

        self.powers = self.character.powers
        self.current_power_index = 0
        if self.powers:
            self.selected_power = self.powers[self.current_power_index]
        else:
            self.selected_power = None

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
                if event.key == pygame.K_SPACE and self.selected_power:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - self.x
                    dy = mouse_y - self.y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        dx, dy = dx / dist, dy / dist
                    new_projectiles.append(Projectile(self.x, self.y, dx, dy, self.selected_power))

                # Switch powers with number keys
                key_to_power_index = {
                    pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4,
                    pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8,
                }
                if event.key in key_to_power_index:
                    power_index = key_to_power_index[event.key]
                    if power_index < len(self.powers):
                        self.current_power_index = power_index
                        self.selected_power = self.powers[power_index]
                        print(f"Switched to {self.selected_power.name}")

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

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            return True
        return False

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        print(f"Leveled up to level {self.level}!")

    def recalculate_stats(self):
        self.stats = self.character.stats.copy()
        for item in self.equipment.values():
            for stat, value in item.stats.items():
                self.stats[stat] = self.stats.get(stat, 0) + value

    def draw(self, screen):
        screen.blit(self.image, self.rect)
