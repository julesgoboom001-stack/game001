class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Equipment(Item):
    def __init__(self, name, slot, stats, value):
        super().__init__(name, value)
        self.slot = slot
        self.stats = stats

# --- Resources ---
copper_ore = Item(name="Copper Ore", value=1)
bronze_bar = Item(name="Bronze Bar", value=5)

# --- Equipment ---
bronze_sword = Equipment(name="Bronze Sword", slot="weapon", stats={"damage": 5}, value=20)
shield = Equipment(name="Shield", slot="offhand", stats={"defense": 5}, value=15)
helmet = Equipment(name="Helmet", slot="head", stats={"health": 10}, value=10)

# A dictionary for easy access to all items
all_items = {
    "copper_ore": copper_ore,
    "bronze_bar": bronze_bar,
    "bronze_sword": bronze_sword,
    "shield": shield,
    "helmet": helmet,
}
