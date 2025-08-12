class Item:
    def __init__(self, name):
        self.name = name

class Equipment(Item):
    def __init__(self, name, slot, stats):
        super().__init__(name)
        self.slot = slot
        self.stats = stats

# --- Resources ---
copper_ore = Item(name="Copper Ore")
bronze_bar = Item(name="Bronze Bar")

# --- Equipment ---
bronze_sword = Equipment(name="Bronze Sword", slot="weapon", stats={"damage": 5})
shield = Equipment(name="Shield", slot="offhand", stats={"defense": 5})
helmet = Equipment(name="Helmet", slot="head", stats={"health": 10})

# A dictionary for easy access to all items
all_items = {
    "copper_ore": copper_ore,
    "bronze_bar": bronze_bar,
    "bronze_sword": bronze_sword,
    "shield": shield,
    "helmet": helmet,
}
