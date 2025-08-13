import random
from map import GameMap, Tile

class WorldGenerator:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

    def generate_map(self):
        game_map = GameMap(self.map_width, self.map_height)

        # All tiles start as walls
        for y in range(self.map_height):
            for x in range(self.map_width):
                game_map.tiles[x][y].blocked = True
                game_map.tiles[x][y].block_sight = True

        # Random walk
        max_tunnels = 10
        max_length = 8

        for i in range(max_tunnels):
            x = random.randint(1, self.map_width - 2)
            y = random.randint(1, self.map_height - 2)
            last_direction = None

            for j in range(max_length):
                direction = random.randint(0, 3)
                if last_direction is not None:
                    # Prefer to continue in the same direction
                    if random.randint(0, 100) > 25:
                        direction = last_direction

                if direction == 0: # North
                    if y > 1: y -= 1
                elif direction == 1: # East
                    if x < self.map_width - 2: x += 1
                elif direction == 2: # South
                    if y < self.map_height - 2: y += 1
                elif direction == 3: # West
                    if x > 1: x -= 1

                if game_map.tiles[x][y].blocked:
                    game_map.tiles[x][y].blocked = False
                    game_map.tiles[x][y].block_sight = False

                last_direction = direction

        return game_map
