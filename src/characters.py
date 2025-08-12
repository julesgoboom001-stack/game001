# src/characters.py

class Character:
    def __init__(self, name, stats, sprite, sprite_walk):
        self.name = name
        self.stats = stats
        self.sprite = sprite
        self.sprite_walk = sprite_walk

class Warrior(Character):
    def __init__(self):
        super().__init__(
            name="Warrior",
            stats={"strength": 10, "dexterity": 5, "intelligence": 3},
            sprite="assets/sprites/warrior.ppm",
            sprite_walk="assets/sprites/warrior_walk.ppm"
        )

class Mage(Character):
    def __init__(self):
        super().__init__(
            name="Mage",
            stats={"strength": 3, "dexterity": 5, "intelligence": 10},
            sprite="assets/sprites/mage.ppm",
            sprite_walk="assets/sprites/mage_walk.ppm"
        )

class Rogue(Character):
    def __init__(self):
        super().__init__(
            name="Rogue",
            stats={"strength": 5, "dexterity": 10, "intelligence": 5},
            sprite="assets/sprites/rogue.ppm",
            sprite_walk="assets/sprites/rogue_walk.ppm"
        )

# A dictionary to easily access all character classes
character_classes = {
    "Warrior": Warrior,
    "Mage": Mage,
    "Rogue": Rogue,
}
