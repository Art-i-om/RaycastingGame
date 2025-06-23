import json

import pygame

_ = False
mini_map = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, 2, 2, _, _, _, _, _, 1, 1, 1, 3],
    [3, _, _, _, _, _, 2, _, _, _, _, _, 1, _, _, 3],
    [3, _, _, _, _, _, 2, 2, _, _, _, 1, 1, _, _, 3],
    [3, _, 1, 1, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

DEFAULT_MAP_PATH = "maps/default.map"

class Map:
    def __init__(self, game, path=DEFAULT_MAP_PATH):
        self.game = game
        self.mini_map = []
        self.world_map = {}
        self.get_map()
        if path:
            self.load_from_file(path)

    def load_from_file(self, path):
        self.mini_map = []
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("["):
                        row = json.loads(line)
                    else:
                        row = [int(x) for x in line.replace(",", " ").split()]
                    self.mini_map.append(row)
        except FileNotFoundError:
            self.mini_map = []

        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pygame.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]