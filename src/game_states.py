import pygame
from characters import character_classes
from client import GameClient
from items import all_items

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

class MainMenu(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.options = ["Single Player", "Multiplayer"]
        self.selected_index = 0

    def on_enter(self, data=None):
        print("Entering Main Menu")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_index == 0: # Single Player
                        self.state_manager.set_state("CHARACTER_SELECTION")
                    elif self.selected_index == 1: # Multiplayer
                        self.state_manager.set_state("CHARACTER_SELECTION", {"multiplayer": True})

    def draw(self, screen):
        screen.fill((50, 50, 50))
        title_text = self.font.render("Diablo-like Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(400, 100))
        screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, 200 + i * 50))
            screen.blit(text, text_rect)


class CharacterSelection(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.character_names = list(character_classes.keys())
        self.selected_index = 0
        self.is_multiplayer = False

    def on_enter(self, data=None):
        print("Entering Character Selection")
        if data and data.get("multiplayer"):
            self.is_multiplayer = True
        else:
            self.is_multiplayer = False

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
                    if self.is_multiplayer:
                        gameplay_state = self.state_manager.states["GAMEPLAY"]
                        client = GameClient(on_message_received=gameplay_state.handle_server_message)
                        if client.connect():
                            client.send_message("new_player", {"character_name": selected_character_name})
                            self.state_manager.set_state("GAMEPLAY", {
                                "character_name": selected_character_name,
                                "client": client
                            })
                        else:
                            print("Could not connect to server.")
                            self.state_manager.set_state("MAIN_MENU")
                    else:
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
from skills import ResourceNode

class Gameplay(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.resource_nodes = []
        self.font = pygame.font.Font(None, 36)
        self.client = None
        self.other_players = {}
        self.last_player_pos = (0, 0)
        self.chat_active = False
        self.chat_input = ""
        self.chat_messages = []
        self.trade_request_pending = False
        self.incoming_trade_from = None
        self.team_members = []
        self.incoming_team_invite_from = None
        self.my_player_id = None

    def on_enter(self, data=None):
        print("Entering Gameplay")
        if data and "client" in data:
            self.client = data["client"]
            self.client.on_message_received = self.handle_server_message
            print("Multiplayer mode activated.")
        if data and "player" in data:
            self.player = data["player"]
        elif data and "character_name" in data:
            character_name = data["character_name"]
            print(f"Selected character: {character_name}")
            character_data = character_classes[character_name]()
            self.player = Player(character_data)

            self.enemies.append(Enemy(100, 100))
            self.resource_nodes.append(
                ResourceNode(200, 200, item_yield=all_items["copper_ore"], skill="mining", xp_gain=10, sprite_path="assets/sprites/copper_vein.ppm")
            )
        else:
            print("No character selected, returning to selection.")
            self.state_manager.set_state("CHARACTER_SELECTION")

    def on_exit(self):
        print("Exiting Gameplay")
        # Don't clear everything, so we can return from other states
        # self.enemies = []
        # self.projectiles = []
        # self.resource_nodes = []

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    self.chat_active = not self.chat_active
                    if not self.chat_active:
                        self.chat_input = "" # Clear input when deactivating
                elif self.chat_active:
                    if event.key == pygame.K_RETURN:
                        if self.chat_input:
                            self.client.send_message("chat_message", {"message": self.chat_input})
                            self.chat_input = ""
                            self.chat_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.chat_input = self.chat_input[:-1]
                    else:
                        self.chat_input += event.unicode
                    return # Stop further event processing while typing

        if not self.chat_active:
            if self.player:
                new_projectiles = self.player.handle_events(events)
                self.projectiles.extend(new_projectiles)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.state_manager.set_state("INVENTORY", {"player": self.player})
                    elif event.key == pygame.K_c:
                        self.state_manager.set_state("CRAFTING", {"player": self.player})
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.client and not self.trade_request_pending:
                            # Find nearest player
                            nearest_player_id = None
                            min_dist = float('inf')
                            for player_id, player_data in self.other_players.items():
                                if player_id == self.my_player_id: continue
                                dist = ((self.player.x - player_data['x'])**2 + (self.player.y - player_data['y'])**2)**0.5
                                if dist < min_dist:
                                    min_dist = dist
                                    nearest_player_id = player_id

                            if nearest_player_id and min_dist < 100: # Trade if within 100 pixels
                                self.client.send_message("trade_request", {"target_id": nearest_player_id})
                                self.trade_request_pending = True
                                print(f"Sent trade request to {nearest_player_id}")
                    elif event.key == pygame.K_p: # Invite to party/team
                        if self.client:
                            # Find nearest player
                            nearest_player_id = None
                            min_dist = float('inf')
                            for player_id, player_data in self.other_players.items():
                                if player_id == self.my_player_id: continue
                                dist = ((self.player.x - player_data['x'])**2 + (self.player.y - player_data['y'])**2)**0.5
                                if dist < min_dist:
                                    min_dist = dist
                                    nearest_player_id = player_id

                            if nearest_player_id and min_dist < 100:
                                self.client.send_message("team_invite", {"target_id": nearest_player_id})
                                print(f"Sent team invite to {nearest_player_id}")

                    elif event.key == pygame.K_y:
                        if self.incoming_trade_from:
                            self.client.send_message("trade_accepted", {"requester_id": self.incoming_trade_from})
                            self.incoming_trade_from = None
                        elif self.incoming_team_invite_from:
                            self.client.send_message("team_invite_accepted", {"requester_id": self.incoming_team_invite_from})
                            self.incoming_team_invite_from = None

                    elif event.key == pygame.K_n:
                        if self.incoming_trade_from:
                            self.client.send_message("trade_declined", {"requester_id": self.incoming_trade_from})
                            self.incoming_trade_from = None
                        elif self.incoming_team_invite_from:
                            self.client.send_message("team_invite_declined", {"requester_id": self.incoming_team_invite_from})
                            self.incoming_team_invite_from = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        for node in self.resource_nodes[:]:
                            if node.rect.collidepoint(event.pos):
                                self.player.inventory.append(node.item_yield)
                                self.player.skills[node.skill].add_xp(node.xp_gain)
                                print(f"Mined {node.item_yield.name}! Gained {node.xp_gain} {node.skill} XP.")
                                self.resource_nodes.remove(node)

    def update(self):
        if self.player:
            self.player.update()
            if self.client:
                if not self.my_player_id and self.client.my_id:
                    self.my_player_id = self.client.my_id
                new_pos = (self.player.x, self.player.y)
                if new_pos != self.last_player_pos:
                    self.client.send_message("player_moved", {"x": new_pos[0], "y": new_pos[1]})
                    self.last_player_pos = new_pos
        for enemy in self.enemies:
            enemy.update(self.player)
        for projectile in self.projectiles:
            projectile.update()

        # Combat logic
        for projectile in self.projectiles[:]:
            # Check for collisions with other players
            if self.client:
                for player_id, player_data in self.other_players.items():
                    player_rect = pygame.Rect(player_data['x'], player_data['y'], 32, 32)
                    if projectile.rect.colliderect(player_rect):
                        # Friendly fire is off, so we just remove the projectile
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)
                        break # Projectile can only hit one thing
                else: # continue if the inner loop wasn't broken
                    continue
                break # exit outer loop if projectile was removed

            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.health -= projectile.damage
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    if enemy.health <= 0:
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                            if self.player:
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

    def handle_server_message(self, data):
        message_type = data.get("type")
        payload = data.get("payload")
        print(f"Client received: {message_type} - {payload}")

        if message_type == "current_players":
            self.other_players = payload
        elif message_type == "player_joined":
            self.other_players[payload["id"]] = payload
        elif message_type == "player_left":
            if payload["id"] in self.other_players:
                del self.other_players[payload["id"]]
        elif message_type == "player_moved":
            player_id = payload["id"]
            if player_id in self.other_players:
                self.other_players[player_id]["x"] = payload["x"]
                self.other_players[player_id]["y"] = payload["y"]
        elif message_type == "new_chat_message":
            self.chat_messages.append(payload["message"])
            if len(self.chat_messages) > 10: # Keep only the last 10 messages
                self.chat_messages.pop(0)
        elif message_type == "incoming_trade_request":
            self.incoming_trade_from = payload["from_id"]
        elif message_type == "trade_declined":
            self.trade_request_pending = False
            print("Trade declined.")
        elif message_type == "trade_started":
            self.state_manager.set_state("TRADING", {"trade_id": payload["trade_id"], "other_player_id": payload["other_player_id"]})
        elif message_type == "incoming_team_invite":
            self.incoming_team_invite_from = payload["from_id"]
        elif message_type == "team_update":
            self.team_members = payload["members"]
            print(f"Team updated: {self.team_members}")

    def draw(self, screen):
        screen.fill((0, 100, 0))
        for node in self.resource_nodes:
            node.draw(screen)

        for player_id, player_data in self.other_players.items():
            if self.client and player_id != self.my_player_id: # Don't draw self
                color = (0, 0, 255) # Default color for other players
                if player_id in self.team_members:
                    color = (0, 255, 0) # Green for team members
                pygame.draw.rect(screen, color, (player_data['x'], player_data['y'], 32, 32))

        if self.player:
            self.player.draw(screen)
            health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
            screen.blit(health_text, (10, 10))
            level_text = self.font.render(f"Level: {self.player.level}", True, (255, 255, 255))
            screen.blit(level_text, (10, 40))
            xp_text = self.font.render(f"XP: {self.player.xp} / {self.player.xp_to_next_level}", True, (255, 255, 255))
            screen.blit(xp_text, (10, 70))
            if self.player.selected_power:
                power_text = self.font.render(f"Power: {self.player.selected_power.name}", True, (255, 255, 255))
                screen.blit(power_text, (10, 560))

        for enemy in self.enemies:
            enemy.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)

        # Draw chat
        if self.chat_active:
            pygame.draw.rect(screen, (0, 0, 0), (10, 560, 780, 30))
            chat_text = self.font.render(self.chat_input, True, (255, 255, 255))
            screen.blit(chat_text, (15, 565))

        for i, msg in enumerate(self.chat_messages):
            chat_msg_text = self.font.render(msg, True, (255, 255, 255))
            screen.blit(chat_msg_text, (15, 530 - i * 30))

        if self.incoming_trade_from:
            pygame.draw.rect(screen, (50, 50, 50), (250, 250, 300, 100))
            from_player_name = self.other_players.get(self.incoming_trade_from, {}).get('character', 'Unknown')
            trade_req_text = self.font.render(f"Trade request from {from_player_name}", True, (255, 255, 255))
            screen.blit(trade_req_text, (260, 260))

            # Accept button
            pygame.draw.rect(screen, (0, 255, 0), (270, 300, 100, 40))
            accept_text = self.font.render("Accept (Y)", True, (0, 0, 0))
            screen.blit(accept_text, (275, 310))

            # Decline button
            pygame.draw.rect(screen, (255, 0, 0), (430, 300, 100, 40))
            decline_text = self.font.render("Decline (N)", True, (0, 0, 0))
            screen.blit(decline_text, (435, 310))

        if self.incoming_team_invite_from:
            pygame.draw.rect(screen, (50, 50, 50), (250, 250, 300, 100))
            from_player_name = self.other_players.get(self.incoming_team_invite_from, {}).get('character', 'Unknown')
            invite_text = self.font.render(f"Team invite from {from_player_name}", True, (255, 255, 255))
            screen.blit(invite_text, (260, 260))

            # Accept button
            pygame.draw.rect(screen, (0, 255, 0), (270, 300, 100, 40))
            accept_text = self.font.render("Accept (Y)", True, (0, 0, 0))
            screen.blit(accept_text, (275, 310))

            # Decline button
            pygame.draw.rect(screen, (255, 0, 0), (430, 300, 100, 40))
            decline_text = self.font.render("Decline (N)", True, (0, 0, 0))
            screen.blit(decline_text, (435, 310))

from powers import all_powers

class LevelUp(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
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

from recipes import recipes

class Crafting(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.recipes = recipes
        self.selected_index = 0
        self.player = None

    def on_enter(self, data=None):
        print("Entering Crafting screen")
        self.player = data.get("player") if data else None

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: # Press 'c' to exit
                    self.state_manager.set_state("GAMEPLAY", {"player": self.player})
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.recipes)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.recipes)
                elif event.key == pygame.K_RETURN: # Craft item
                    if self.player:
                        selected_recipe = self.recipes[self.selected_index]

                        # Check if player has materials
                        can_craft = True
                        for item_name, required_amount in selected_recipe.materials.items():
                            current_amount = sum(1 for item in self.player.inventory if item.name.lower().replace(" ", "_") == item_name)
                            if current_amount < required_amount:
                                can_craft = False
                                break

                        if can_craft:
                            # Consume materials
                            for item_name, required_amount in selected_recipe.materials.items():
                                for _ in range(required_amount):
                                    for item in self.player.inventory:
                                        if item.name.lower().replace(" ", "_") == item_name:
                                            self.player.inventory.remove(item)
                                            break

                            # Add crafted item
                            self.player.inventory.append(selected_recipe.result_item)
                            print(f"Crafted {selected_recipe.name}!")
                        else:
                            print("Not enough materials.")

    def draw(self, screen):
        screen.fill((80, 40, 20)) # Brown background

        title_text = self.font.render("Crafting", True, (255, 255, 255))
        screen.blit(title_text, (350, 20))

        for i, recipe in enumerate(self.recipes):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(recipe.name, True, color)
            screen.blit(text, (100, 80 + i * 40))

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
                if event.key == pygame.K_i:
                    self.state_manager.set_state("GAMEPLAY", {"player": self.player})
                elif event.key == pygame.K_UP:
                    if self.player and self.player.inventory:
                        self.selected_index = (self.selected_index - 1) % len(self.player.inventory)
                elif event.key == pygame.K_DOWN:
                    if self.player and self.player.inventory:
                        self.selected_index = (self.selected_index + 1) % len(self.player.inventory)
                elif event.key == pygame.K_RETURN:
                    if self.player and self.player.inventory:
                        item_to_equip = self.player.inventory[self.selected_index]
                        from items import Equipment
                        if isinstance(item_to_equip, Equipment):
                            if item_to_equip.slot in self.player.equipment:
                                self.player.inventory.append(self.player.equipment[item_to_equip.slot])

                            self.player.equipment[item_to_equip.slot] = item_to_equip
                            self.player.inventory.pop(self.selected_index)
                            self.player.recalculate_stats()
                            print(f"Equipped {item_to_equip.name}")

    def draw(self, screen):
        screen.fill((20, 20, 80))
        title_text = self.font.render("Inventory", True, (255, 255, 255))
        screen.blit(title_text, (350, 20))
        inv_title = self.font.render("Inventory", True, (255, 255, 255))
        screen.blit(inv_title, (100, 80))
        if self.player:
            for i, item in enumerate(self.player.inventory):
                color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
                item_text = self.font.render(item.name, True, color)
                screen.blit(item_text, (100, 120 + i * 40))
        eq_title = self.font.render("Equipment", True, (255, 255, 255))
        screen.blit(eq_title, (500, 80))
        if self.player:
            y_offset = 0
            for slot, item in self.player.equipment.items():
                item_text = self.font.render(f"{slot}: {item.name}", True, (255, 255, 255))
                screen.blit(item_text, (500, 120 + y_offset * 40))
                y_offset += 1

class Trading(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.trade_id = None
        self.other_player_id = None
        self.my_offer = []
        self.other_player_offer = []
        self.my_offer_locked = False
        self.other_player_offer_locked = False
        self.my_trade_confirmed = False
        self.other_player_trade_confirmed = False
        self.player = None

    def on_enter(self, data=None):
        print("Entering Trading screen")
        self.trade_id = data.get("trade_id")
        self.other_player_id = data.get("other_player_id")

        # We need access to the player object to get the inventory
        self.player = self.state_manager.states["GAMEPLAY"].player

        # We also need the client to send and receive messages
        self.client = self.state_manager.states["GAMEPLAY"].client
        if self.client:
            self.client.on_message_received = self.handle_server_message

    def handle_server_message(self, data):
        message_type = data.get("type")
        payload = data.get("payload")
        print(f"Trading received: {message_type} - {payload}")
        if message_type == "trade_offer_update":
            self.other_player_offer = payload["offer"]
        elif message_type == "trade_finalized":
            print("Trade finalized!")
            received_item_names = payload["received_items"]
            for item_name in received_item_names:
                # Find the item object from the all_items dictionary
                for item_key, item_obj in all_items.items():
                    if item_obj.name == item_name:
                        self.player.inventory.append(item_obj)
                        break
            self.my_offer = []
            self.state_manager.set_state("GAMEPLAY")
        elif message_type == "trade_canceled":
            print("Trade canceled.")
            self.player.inventory.extend(self.my_offer)
            self.my_offer = []
            self.state_manager.set_state("GAMEPLAY")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    # Check if an item in the inventory was clicked
                    if self.player:
                        for i, item in enumerate(self.player.inventory):
                            item_rect = pygame.Rect(50, 120 + i * 40, 200, 30)
                            if item_rect.collidepoint(event.pos):
                                self.my_offer.append(item)
                                self.player.inventory.pop(i)
                                self.client.send_message("trade_offer_update", {"trade_id": self.trade_id, "offer": [item.name for item in self.my_offer]})
                                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Exit trade
                    self.player.inventory.extend(self.my_offer)
                    self.my_offer = []
                    self.client.send_message("trade_cancel", {"trade_id": self.trade_id})
                    self.state_manager.set_state("GAMEPLAY")
                elif event.key == pygame.K_c: # Confirm trade
                    self.client.send_message("trade_confirm", {"trade_id": self.trade_id})


    def draw(self, screen):
        screen.fill((20, 80, 20))
        title_text = self.font.render("Trading", True, (255, 255, 255))
        screen.blit(title_text, (350, 20))

        # Your Inventory
        inv_title = self.font.render("Your Inventory", True, (255, 255, 255))
        screen.blit(inv_title, (50, 80))
        if self.player:
            for i, item in enumerate(self.player.inventory):
                item_text = self.font.render(item.name, True, (255, 255, 255))
                screen.blit(item_text, (50, 120 + i * 40))

        # Your Offer
        your_offer_title = self.font.render("Your Offer", True, (255, 255, 255))
        screen.blit(your_offer_title, (300, 80))
        for i, item in enumerate(self.my_offer):
            item_text = self.font.render(item.name, True, (255, 255, 0))
            screen.blit(item_text, (300, 120 + i * 40))

        # Other Player's Offer
        other_offer_title = self.font.render("Their Offer", True, (255, 255, 255))
        screen.blit(other_offer_title, (550, 80))
        for i, item_name in enumerate(self.other_player_offer):
            item_text = self.font.render(item_name, True, (255, 255, 0))
            screen.blit(item_text, (550, 120 + i * 40))

        # Confirm Button
        pygame.draw.rect(screen, (0, 255, 0), (350, 500, 150, 50))
        confirm_text = self.font.render("Confirm (C)", True, (0, 0, 0))
        screen.blit(confirm_text, (360, 515))
