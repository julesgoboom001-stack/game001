import pygame
from characters import character_classes

class StateManager:
    def __init__(self, screen):
        self.screen = screen
        self.states = {}
        self.current_state_name = None
        self.current_state = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def set_state(self, state_name, data=None):
        if self.current_state:
            self.current_state.on_exit()
        self.current_state_name = state_name
        self.current_state = self.states[state_name]
        self.current_state.on_enter(data)

    def handle_events(self, events):
        self.current_state.handle_events(events)

    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw(self.screen)

class BaseState:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def on_enter(self, data=None):
        pass

    def on_exit(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        pass

    def draw(self, screen):
        pass

class CharacterSelection(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.character_names = list(character_classes.keys())
        self.selected_index = 0

    def on_enter(self, data=None):
        print("Entering Character Selection")

    def on_exit(self):
        print("Exiting Character Selection")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.character_names)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.character_names)
                elif event.key == pygame.K_RETURN:
                    selected_character_name = self.character_names[self.selected_index]
                    self.state_manager.set_state("GAMEPLAY", {"character_name": selected_character_name})

    def draw(self, screen):
        screen.fill((100, 100, 100))
        title_text = self.font.render("Select Your Character", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(400, 100))
        screen.blit(title_text, title_rect)

        for i, name in enumerate(self.character_names):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(name, True, color)
            text_rect = text.get_rect(center=(400, 200 + i * 50))
            screen.blit(text, text_rect)

from player import Player
from enemy import Enemy
from projectile import Projectile
from items import all_items

class Gameplay(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.font = pygame.font.Font(None, 36)

    def on_enter(self, data=None):
        print("Entering Gameplay")
        if data and "player" in data:
            # Continue with existing player (e.g., after level up)
            self.player = data["player"]
        elif data and "character_name" in data:
            # Start a new game
            character_name = data["character_name"]
            print(f"Selected character: {character_name}")
            character_data = character_classes[character_name]()
            self.player = Player(character_data)

            # Spawn an enemy
            self.enemies.append(Enemy(100, 100))
        else:
            # Should not happen, but as a fallback, go to character selection
            print("No character selected, returning to selection.")
            self.state_manager.set_state("CHARACTER_SELECTION")

    def on_exit(self):
        print("Exiting Gameplay")
        self.enemies = []
        self.projectiles = []

    def handle_events(self, events):
        super().handle_events(events)
        if self.player:
            new_projectiles = self.player.handle_events(events)
            self.projectiles.extend(new_projectiles)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.state_manager.set_state("INVENTORY", {"player": self.player})

    def update(self):
        if self.player:
            self.player.update()
        for enemy in self.enemies:
            enemy.update(self.player)
        for projectile in self.projectiles:
            projectile.update()

        # Combat logic
        for projectile in self.projectiles[:]: # Iterate over a copy
            for enemy in self.enemies[:]: # Iterate over a copy
                if projectile.rect.colliderect(enemy.rect):
                    enemy.health -= projectile.damage
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    if enemy.health <= 0:
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                            if self.player:
                                # Add loot to player's inventory
                                self.player.inventory.append(all_items["sword"])
                                print("You got a sword!")

                                if self.player.add_xp(enemy.xp_value):
                                    self.player.level_up()
                                    self.state_manager.set_state("LEVEL_UP", {"player": self.player})

        # Player damage logic
        if self.player:
            for enemy in self.enemies:
                if enemy.is_attacking and enemy.rect.colliderect(self.player.rect):
                    self.player.health -= 1

        # Remove projectiles that are off-screen
        self.projectiles = [p for p in self.projectiles if 0 < p.x < 800 and 0 < p.y < 600]

        # Player death logic
        if self.player and self.player.health <= 0:
            self.state_manager.set_state("CHARACTER_SELECTION")

    def draw(self, screen):
        screen.fill((0, 100, 0)) # Green background
        if self.player:
            self.player.draw(screen)
            # Draw player health
            health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
            screen.blit(health_text, (10, 10))
            # Draw player level and xp
            level_text = self.font.render(f"Level: {self.player.level}", True, (255, 255, 255))
            screen.blit(level_text, (10, 40))
            xp_text = self.font.render(f"XP: {self.player.xp} / {self.player.xp_to_next_level}", True, (255, 255, 255))
            screen.blit(xp_text, (10, 70))
            # Draw selected power
            if self.player.selected_power:
                power_text = self.font.render(f"Power: {self.player.selected_power.name}", True, (255, 255, 255))
                screen.blit(power_text, (10, 560))

        for enemy in self.enemies:
            enemy.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)

from powers import all_powers

class LevelUp(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        # For now, a hardcoded list of powers to learn
        self.available_powers = list(all_powers.values())
        self.selected_index = 0
        self.player = None

    def on_enter(self, data=None):
        print("Entering Level Up screen")
        self.player = data.get("player") if data else None

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.available_powers)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.available_powers)
                elif event.key == pygame.K_RETURN:
                    if self.player:
                        selected_power = self.available_powers[self.selected_index]
                        if selected_power not in self.player.powers:
                            self.player.powers.append(selected_power)
                            print(f"Learned new power: {selected_power.name}")
                        else:
                            print(f"Already know {selected_power.name}")
                    # This should pass back the player object to the gameplay state
                    self.state_manager.set_state("GAMEPLAY", {"player": self.player})

    def draw(self, screen):
        screen.fill((50, 50, 50))
        title_text = self.font.render("Level Up! Choose a new power:", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(400, 100))
        screen.blit(title_text, title_rect)

        for i, power in enumerate(self.available_powers):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(power.name, True, color)
            text_rect = text.get_rect(center=(400, 200 + i * 50))
            screen.blit(text, text_rect)

class Inventory(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.player = None
        self.selected_index = 0

    def on_enter(self, data=None):
        print("Entering Inventory screen")
        self.player = data.get("player") if data else None

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i: # Press 'i' to exit
                    self.state_manager.set_state("GAMEPLAY", {"player": self.player})
                elif event.key == pygame.K_UP:
                    if self.player and self.player.inventory:
                        self.selected_index = (self.selected_index - 1) % len(self.player.inventory)
                elif event.key == pygame.K_DOWN:
                    if self.player and self.player.inventory:
                        self.selected_index = (self.selected_index + 1) % len(self.player.inventory)
                elif event.key == pygame.K_RETURN: # Equip item
                    if self.player and self.player.inventory:
                        item_to_equip = self.player.inventory[self.selected_index]
                        # For now, only equip Equipment
                        from items import Equipment
                        if isinstance(item_to_equip, Equipment):
                            # Unequip any existing item in the same slot
                            if item_to_equip.slot in self.player.equipment:
                                self.player.inventory.append(self.player.equipment[item_to_equip.slot])

                            self.player.equipment[item_to_equip.slot] = item_to_equip
                            self.player.inventory.pop(self.selected_index)
                            self.player.recalculate_stats()
                            print(f"Equipped {item_to_equip.name}")

    def draw(self, screen):
        screen.fill((20, 20, 80)) # Dark blue background

        # Draw Title
        title_text = self.font.render("Inventory", True, (255, 255, 255))
        screen.blit(title_text, (350, 20))

        # Draw Inventory
        inv_title = self.font.render("Inventory", True, (255, 255, 255))
        screen.blit(inv_title, (100, 80))
        if self.player:
            for i, item in enumerate(self.player.inventory):
                color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
                item_text = self.font.render(item.name, True, color)
                screen.blit(item_text, (100, 120 + i * 40))

        # Draw Equipment
        eq_title = self.font.render("Equipment", True, (255, 255, 255))
        screen.blit(eq_title, (500, 80))
        if self.player:
            y_offset = 0
            for slot, item in self.player.equipment.items():
                item_text = self.font.render(f"{slot}: {item.name}", True, (255, 255, 255))
                screen.blit(item_text, (500, 120 + y_offset * 40))
                y_offset += 1
