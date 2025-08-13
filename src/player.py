import pygame
from projectile import Projectile
import math
from items import all_items
from skills import Skill
from powers import get_elemental_power

class Player:
    def __init__(self, character, element):
        self.character = character
        self.element = element
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
        self.apply_elemental_bonus()
        self.health = self.stats["health"]

        self.x = 400
        self.y = 300
        self.speed = 5

        self.powers = [get_elemental_power(p, self.element) for p in self.character.powers]
        self.current_power_index = 0
        if self.powers:
            self.selected_power = self.powers[self.current_power_index]
        else:
            self.selected_power = None
        self.cooldown_timer = 0

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
                if event.key == pygame.K_SPACE and self.selected_power and self.cooldown_timer == 0:
                    cooldown_reduction = self.stats.get("cooldown_reduction", 0)
                    actual_cooldown = self.selected_power.cooldown * (1 - cooldown_reduction)
                    self.cooldown_timer = int(actual_cooldown)
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
        # Cooldown timer
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

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

    def apply_elemental_bonus(self):
        # Warrior Bonuses
        if self.character.name == "Warrior":
            if self.element == "Fire":
                self.stats['strength'] = int(self.stats['strength'] * 1.15)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.10)
            elif self.element == "Poison":
                self.stats['dexterity'] = int(self.stats['dexterity'] * 1.10)
            elif self.element == "Water":
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10
            elif self.element == "Air":
                self.speed *= 1.10
            elif self.element == "Dark":
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.02
            elif self.element == "Light":
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05

        # Paladin Bonuses
        elif self.character.name == "Paladin":
            if self.element == "Fire":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.15)
            elif self.element == "Poison":
                self.stats['health'] = int(self.stats['health'] * 1.10)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.20)
            elif self.element == "Air":
                self.speed *= 1.05
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.05
            elif self.element == "Dark":
                self.stats['strength'] = int(self.stats['strength'] * 1.20)
                self.stats['health'] = int(self.stats['health'] * 0.90)
            elif self.element == "Light":
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.10

        # Brute Bonuses
        elif self.character.name == "Brute":
            if self.element == "Fire":
                self.stats['strength'] = int(self.stats['strength'] * 1.25)
            elif self.element == "Earth":
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.20
            elif self.element == "Poison":
                self.stats['thorns'] = self.stats.get('thorns', 0) + 5
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.25)
            elif self.element == "Air":
                self.speed *= 1.15
            elif self.element == "Dark":
                self.stats['strength'] = int(self.stats['strength'] * 1.40)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) - 0.10
            elif self.element == "Light":
                self.stats['health'] = int(self.stats['health'] * 1.20)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05

        # Priest Bonuses
        elif self.character.name == "Priest":
            if self.element == "Fire":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.20)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.15)
            elif self.element == "Poison":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.10)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05
            elif self.element == "Water":
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.15
            elif self.element == "Air":
                self.speed *= 1.10
            elif self.element == "Dark":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.30)
                self.stats['health'] = int(self.stats['health'] * 0.90)
            elif self.element == "Light":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.10)
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10

        # Shaman Bonuses
        elif self.character.name == "Shaman":
            if self.element == "Fire":
                self.stats['strength'] = int(self.stats['strength'] * 1.10)
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.10)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.20)
            elif self.element == "Poison":
                self.stats['dexterity'] = int(self.stats['dexterity'] * 1.10)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.15)
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10
            elif self.element == "Air":
                self.speed *= 1.15
            elif self.element == "Dark":
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Light":
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.10

        # Druid Bonuses
        elif self.character.name == "Druid":
            if self.element == "Fire":
                self.stats['dexterity'] = int(self.stats['dexterity'] * 1.15)
                self.stats['strength'] = int(self.stats['strength'] * 1.10)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.25)
            elif self.element == "Poison":
                self.stats['dexterity'] = int(self.stats['dexterity'] * 1.15)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.15)
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10
            elif self.element == "Air":
                self.speed *= 1.20
            elif self.element == "Dark":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.20)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.02
            elif self.element == "Light":
                self.stats['health'] = int(self.stats['health'] * 1.15)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05

        # Beast Master Bonuses
        elif self.character.name == "Beast Master":
            if self.element == "Fire":
                self.stats['dexterity'] = int(self.stats['dexterity'] * 1.15)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.15)
            elif self.element == "Poison":
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.10)
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10
            elif self.element == "Air":
                self.speed *= 1.15
            elif self.element == "Dark":
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.10
            elif self.element == "Light":
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.10

        # Necromancer Bonuses
        elif self.character.name == "Necromancer":
            if self.element == "Fire":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.20)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.20)
            elif self.element == "Poison":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.10)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.10
            elif self.element == "Air":
                self.speed *= 1.10
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10
            elif self.element == "Dark":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.25)
            elif self.element == "Light":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05

        # Demonic Bonuses
        elif self.character.name == "Demonic":
            if self.element == "Fire":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.25)
            elif self.element == "Earth":
                self.stats['strength'] = int(self.stats['strength'] * 1.10)
                self.stats['health'] = int(self.stats['health'] * 1.15)
            elif self.element == "Poison":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.15)
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.10)
            elif self.element == "Air":
                self.speed *= 1.10
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.10)
            elif self.element == "Dark":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.30)
                self.stats['health'] = int(self.stats['health'] * 0.90)
            elif self.element == "Light":
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.15

        # Hunter Bonuses
        elif self.character.name == "Hunter":
            if self.element == "Fire":
                self.stats['dexterity'] = int(self.stats['dexterity'] * 1.15)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.10)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05
            elif self.element == "Poison":
                self.stats['dexterity'] = int(self.stats['dexterity'] * 1.10)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Water":
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.15
            elif self.element == "Air":
                self.speed *= 1.10
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.05
            elif self.element == "Dark":
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.10
            elif self.element == "Light":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.10)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05

        # Wizard Bonuses
        elif self.character.name == "Wizard":
            if self.element == "Fire":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.20)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.20)
            elif self.element == "Poison":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Water":
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10
                self.stats['health'] = int(self.stats['health'] * 1.10)
            elif self.element == "Air":
                self.speed *= 1.15
            elif self.element == "Dark":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.25)
                self.stats['health'] = int(self.stats['health'] * 0.90)
            elif self.element == "Light":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
                self.stats['damage_reduction'] = self.stats.get('damage_reduction', 0) + 0.05

        # Engineer Bonuses
        elif self.character.name == "Engineer":
            if self.element == "Fire":
                self.stats['strength'] = int(self.stats['strength'] * 1.10)
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
            elif self.element == "Earth":
                self.stats['health'] = int(self.stats['health'] * 1.25)
            elif self.element == "Poison":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Water":
                self.stats['health'] = int(self.stats['health'] * 1.10)
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.10
            elif self.element == "Air":
                self.stats['cooldown_reduction'] = self.stats.get('cooldown_reduction', 0) + 0.15
            elif self.element == "Dark":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.20)
                self.stats['lifesteal'] = self.stats.get('lifesteal', 0) + 0.05
            elif self.element == "Light":
                self.stats['intelligence'] = int(self.stats['intelligence'] * 1.15)
                self.stats['health'] = int(self.stats['health'] * 1.10)

        # After applying bonuses, it's good to log the final stats for debugging
        print(f"Final stats for {self.character.name} ({self.element}): {self.stats}")
        print(f"Final speed: {self.speed}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
