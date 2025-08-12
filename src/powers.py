# src/powers.py

class Power:
    def __init__(self, name, damage, range, cooldown, projectile_sprite):
        self.name = name
        self.damage = damage
        self.range = range
        self.cooldown = cooldown
        self.projectile_sprite = projectile_sprite

# Mage Powers
fireball = Power(name="Fireball", damage=10, range=300, cooldown=30, projectile_sprite="assets/sprites/fireball.ppm")
ice_bolt = Power(name="Ice Bolt", damage=5, range=400, cooldown=20, projectile_sprite="assets/sprites/ice_bolt.ppm")

# Rogue Powers
dagger_throw = Power(name="Dagger Throw", damage=7, range=250, cooldown=15, projectile_sprite="assets/sprites/dagger.ppm")

# Warrior Powers
throwing_axe = Power(name="Throwing Axe", damage=15, range=200, cooldown=45, projectile_sprite="assets/sprites/axe.ppm")

# A dictionary to hold all powers, for easy access
all_powers = {
    "fireball": fireball,
    "ice_bolt": ice_bolt,
    "dagger_throw": dagger_throw,
    "throwing_axe": throwing_axe,
}

import copy

def get_elemental_power(base_power, element):
    """
    Takes a base power and an element and returns a new Power instance
    with elemental modifications.
    """
    elemental_power = copy.copy(base_power)

    if element == "Fire":
        elemental_power.name = f"Fire {base_power.name}"
        elemental_power.damage = int(elemental_power.damage * 1.2)
        if "fireball" not in elemental_power.projectile_sprite:
            elemental_power.projectile_sprite = "assets/sprites/fireball.ppm"
    elif element == "Water": # Using ice_bolt for Water
        elemental_power.name = f"Water {base_power.name}"
        if "ice_bolt" not in elemental_power.projectile_sprite:
            elemental_power.projectile_sprite = "assets/sprites/ice_bolt.ppm"
    # Other elements can be added here.

    return elemental_power
