class Item:
    def __init__(self, name):
        self.name = name

class Equipment(Item):
    def __init__(self, name, slot, stats):
        super().__init__(name)
        self.slot = slot
        self.stats = stats

# Example Items
sword = Equipment(name="Sword", slot="weapon", stats={"damage": 5})
shield = Equipment(name="Shield", slot="offhand", stats={"defense": 5})
helmet = Equipment(name="Helmet", slot="head", stats={"health": 10})

# A dictionary for easy access to all items
all_items = {
    "sword": sword,
    "shield": shield,
    "helmet": helmet,
}
