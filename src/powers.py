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
