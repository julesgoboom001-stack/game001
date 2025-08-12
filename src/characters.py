# src/characters.py
from powers import fireball, ice_bolt, dagger_throw, throwing_axe

class Character:
    def __init__(self, name, stats, sprite, sprite_walk, powers):
        self.name = name
        self.stats = stats
        self.sprite = sprite
        self.sprite_walk = sprite_walk
        self.powers = powers

# Tank Classes
class Warrior(Character):
    def __init__(self):
        super().__init__(
            name="Warrior",
            stats={"strength": 10, "dexterity": 5, "intelligence": 3, "health": 150},
            sprite="assets/sprites/warrior.ppm",
            sprite_walk="assets/sprites/warrior_walk.ppm",
            powers=[throwing_axe]
        )

class Paladin(Character):
    def __init__(self):
        super().__init__(
            name="Paladin",
            stats={"strength": 9, "dexterity": 4, "intelligence": 5, "health": 160},
            sprite="assets/sprites/warrior.ppm",
            sprite_walk="assets/sprites/warrior_walk.ppm",
            powers=[throwing_axe]
        )

class Brute(Character):
    def __init__(self):
        super().__init__(
            name="Brute",
            stats={"strength": 12, "dexterity": 3, "intelligence": 2, "health": 180},
            sprite="assets/sprites/warrior.ppm",
            sprite_walk="assets/sprites/warrior_walk.ppm",
            powers=[throwing_axe]
        )

# Range Damage Classes
class Hunter(Character):
    def __init__(self):
        super().__init__(
            name="Hunter",
            stats={"strength": 5, "dexterity": 10, "intelligence": 4, "health": 100},
            sprite="assets/sprites/rogue.ppm",
            sprite_walk="assets/sprites/rogue_walk.ppm",
            powers=[dagger_throw]
        )

class Wizard(Character):
    def __init__(self):
        super().__init__(
            name="Wizard",
            stats={"strength": 3, "dexterity": 5, "intelligence": 10, "health": 80},
            sprite="assets/sprites/mage.ppm",
            sprite_walk="assets/sprites/mage_walk.ppm",
            powers=[fireball, ice_bolt]
        )

class Engineer(Character):
    def __init__(self):
        super().__init__(
            name="Engineer",
            stats={"strength": 4, "dexterity": 7, "intelligence": 8, "health": 90},
            sprite="assets/sprites/mage.ppm",
            sprite_walk="assets/sprites/mage_walk.ppm",
            powers=[fireball] # Placeholder
        )

# Melee Damage Classes
class Rogue(Character):
    def __init__(self):
        super().__init__(
            name="Rogue",
            stats={"strength": 5, "dexterity": 12, "intelligence": 5, "health": 100},
            sprite="assets/sprites/rogue.ppm",
            sprite_walk="assets/sprites/rogue_walk.ppm",
            powers=[dagger_throw]
        )

class Lancer(Character):
    def __init__(self):
        super().__init__(
            name="Lancer",
            stats={"strength": 8, "dexterity": 8, "intelligence": 4, "health": 110},
            sprite="assets/sprites/warrior.ppm",
            sprite_walk="assets/sprites/warrior_walk.ppm",
            powers=[throwing_axe]
        )

class Monk(Character):
    def __init__(self):
        super().__init__(
            name="Monk",
            stats={"strength": 7, "dexterity": 9, "intelligence": 6, "health": 120},
            sprite="assets/sprites/rogue.ppm",
            sprite_walk="assets/sprites/rogue_walk.ppm",
            powers=[dagger_throw] # placeholder
        )

# Pet Controller Classes
class BeastMaster(Character):
    def __init__(self):
        super().__init__(
            name="Beast Master",
            stats={"strength": 6, "dexterity": 7, "intelligence": 6, "health": 110},
            sprite="assets/sprites/rogue.ppm",
            sprite_walk="assets/sprites/rogue_walk.ppm",
            powers=[] # No pet powers yet
        )

class Necromancer(Character):
    def __init__(self):
        super().__init__(
            name="Necromancer",
            stats={"strength": 4, "dexterity": 5, "intelligence": 9, "health": 90},
            sprite="assets/sprites/mage.ppm",
            sprite_walk="assets/sprites/mage_walk.ppm",
            powers=[] # No pet powers yet
        )

class Demonic(Character):
    def __init__(self):
        super().__init__(
            name="Demonic",
            stats={"strength": 7, "dexterity": 6, "intelligence": 7, "health": 100},
            sprite="assets/sprites/mage.ppm",
            sprite_walk="assets/sprites/mage_walk.ppm",
            powers=[] # No pet powers yet
        )

# Healer Classes
class Priest(Character):
    def __init__(self):
        super().__init__(
            name="Priest",
            stats={"strength": 4, "dexterity": 5, "intelligence": 9, "health": 90},
            sprite="assets/sprites/mage.ppm",
            sprite_walk="assets/sprites/mage_walk.ppm",
            powers=[] # No healing powers yet
        )

class Shaman(Character):
    def __init__(self):
        super().__init__(
            name="Shaman",
            stats={"strength": 5, "dexterity": 6, "intelligence": 8, "health": 100},
            sprite="assets/sprites/mage.ppm",
            sprite_walk="assets/sprites/mage_walk.ppm",
            powers=[] # No healing powers yet
        )

class Druid(Character):
    def __init__(self):
        super().__init__(
            name="Druid",
            stats={"strength": 6, "dexterity": 6, "intelligence": 7, "health": 110},
            sprite="assets/sprites/rogue.ppm",
            sprite_walk="assets/sprites/rogue_walk.ppm",
            powers=[] # No healing powers yet
        )


# A dictionary to easily access all character classes
character_classes = {
    "Warrior": Warrior,
    "Paladin": Paladin,
    "Brute": Brute,
    "Hunter": Hunter,
    "Wizard": Wizard,
    "Engineer": Engineer,
    "Rogue": Rogue,
    "Lancer": Lancer,
    "Monk": Monk,
    "Beast Master": BeastMaster,
    "Necromancer": Necromancer,
    "Demonic": Demonic,
    "Priest": Priest,
    "Shaman": Shaman,
    "Druid": Druid,
}
