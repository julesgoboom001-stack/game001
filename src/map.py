import pygame

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        # Create a simple room for testing
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True

        return tiles

    def draw(self, screen, wall_sprite, floor_sprite):
        for x in range(self.width):
            for y in range(self.height):
                wall = self.tiles[x][y].block_sight
                if wall:
                    screen.blit(wall_sprite, (x * 32, y * 32))
                else:
                    screen.blit(floor_sprite, (x * 32, y * 32))
