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

class Gameplay(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.font = pygame.font.Font(None, 36)

    def on_enter(self, data=None):
        print("Entering Gameplay")
        if data and "character_name" in data:
            character_name = data["character_name"]
            print(f"Selected character: {character_name}")
            character_data = character_classes[character_name]()
            self.player = Player(character_data)

            # Spawn an enemy
            self.enemies.append(Enemy(100, 100))
        else:
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
                    enemy.health -= 10
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    if enemy.health <= 0:
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)

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

        for enemy in self.enemies:
            enemy.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)
