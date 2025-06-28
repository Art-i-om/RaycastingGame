import pygame
import csv


class Map:
    def __init__(self, game, path):
        self.game = game
        self.mini_map = []
        self.world_map = {}
        self.sprite_positions = []
        self.npc_positions = []
        self.get_map()
        if path:
            self.load_from_file(path)

    def load_from_file(self, path):
        self.mini_map = []
        try:
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ')
                loaded_data = []
                for row in reader:
                    loaded_data.append([int(tile) for tile in row])
                self.mini_map = loaded_data
        except FileNotFoundError:
            self.mini_map = []

        self.world_map = {}
        self.get_map()

    def get_map(self):
        self.sprite_positions = []
        self.npc_positions = []
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value in (1, 2, 3):
                    self.world_map[(i, j)] = value
                elif value in (4, 5):
                    self.sprite_positions.append(((i + 0.5, j + 0.5), value))
                    row[i] = 0
                elif value == 6:
                    self.npc_positions.append(((i + 0.5, j + 0.5), value))
                    row[i] = 0

    def draw(self):
        [pygame.draw.rect(self.game.display, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]