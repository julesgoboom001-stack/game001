# Project Overview

This document provides a high-level overview of the Diablo-like game project, its architecture, and its core systems.

## Core Architecture

The game is built using Python and the Pygame library. It uses a simple state machine to manage different parts of the game, such as the main menu, gameplay, inventory, etc.

The main components of the architecture are:
- **`main.py`**: The main entry point of the game. It initializes Pygame, creates the state manager, and runs the main game loop.
- **`game_states.py`**: Contains the state manager and the different game state classes. Each state handles its own events, updates, and drawing.
- **Data classes:** Separate classes are used to define game entities like characters, enemies, items, and powers.

## Core Systems

### Character System
- **Classes:** The game has three character classes: Warrior, Mage, and Rogue. Each class is defined in `src/characters.py` and has unique base stats.
- **Progression:** Players gain experience points (XP) by defeating enemies and can level up. Leveling up increases the XP required for the next level and will be used to unlock new powers.

### Combat System
- **Real-time:** Combat is real-time and action-oriented.
- **Player Attacks:** The player can use different attack powers, which are defined in `src/powers.py`. Projectiles are aimed with the mouse.
- **Enemy AI:** Enemies have a simple AI that makes them move towards the player and attack when in range.

### Item System
- **Items and Equipment:** The game has a basic item system with a base `Item` class and an `Equipment` subclass for items that can be worn. Items are defined in `src/items.py`.
- **Inventory:** The player has an inventory to store items.
- **Loot:** Enemies can drop loot when defeated.
- **Stats:** Equipment can modify the player's stats.

### Crafting and Gathering
- **Skills:** The game has a skill system, with Mining and Blacksmithing as the initial skills.
- **Resource Nodes:** The world can contain resource nodes (e.g., ore veins) that can be harvested by the player.
- **Recipes:** Crafting is based on recipes, defined in `src/recipes.py`.
- **Crafting UI:** A basic UI allows the player to see recipes and craft items.

### World Generation
- **Procedural Maps:** The game uses a simple procedural generation algorithm (random walk) to create a new dungeon layout for each game.
- **Tile-based:** The world is represented by a grid of tiles, each with properties like being blocked or allowing sight.
