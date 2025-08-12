import pygame

class Skill:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        print(f"Skill leveled up to level {self.level}!")

class ResourceNode:
    def __init__(self, x, y, item_yield, skill, xp_gain, sprite_path):
        self.x = x
        self.y = y
        self.item_yield = item_yield
        self.skill = skill
        self.xp_gain = xp_gain
        self.sprite = pygame.image.load(sprite_path).convert()
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

class Recipe:
    def __init__(self, name, materials, result_item, skill, required_level):
        self.name = name
        self.materials = materials # e.g., {"copper_ore": 5}
        self.result_item = result_item
        self.skill = skill
        self.required_level = required_level
