import pygame
from game_states import StateManager, MainMenu, CharacterSelection, Gameplay, LevelUp, Inventory, Crafting, Trading

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Window title
pygame.display.set_caption("Diablo-like Game")

def main():
    """Main function."""
    print("Game starting...")
    state_manager = StateManager(screen)

    # Create states
    main_menu_state = MainMenu(state_manager)
    character_selection_state = CharacterSelection(state_manager)
    gameplay_state = Gameplay(state_manager)
    level_up_state = LevelUp(state_manager)
    inventory_state = Inventory(state_manager)
    crafting_state = Crafting(state_manager)
    trading_state = Trading(state_manager)

    # Add states to the manager
    state_manager.add_state("MAIN_MENU", main_menu_state)
    state_manager.add_state("CHARACTER_SELECTION", character_selection_state)
    state_manager.add_state("GAMEPLAY", gameplay_state)
    state_manager.add_state("LEVEL_UP", level_up_state)
    state_manager.add_state("INVENTORY", inventory_state)
    state_manager.add_state("CRAFTING", crafting_state)
    state_manager.add_state("TRADING", trading_state)

    # Set the initial state
    state_manager.set_state("MAIN_MENU")

    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        state_manager.handle_events(events)
        state_manager.update()
        state_manager.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
