from skills import Recipe
from items import copper_ore, bronze_bar, bronze_sword

recipes = [
    Recipe(
        name="Bronze Bar",
        materials={"copper_ore": 2},
        result_item=bronze_bar,
        skill="blacksmithing",
        required_level=1
    ),
    Recipe(
        name="Bronze Sword",
        materials={"bronze_bar": 5},
        result_item=bronze_sword,
        skill="blacksmithing",
        required_level=1
    ),
]
