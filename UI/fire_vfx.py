import pygame
from settings import *
from pygame import gfxdraw
from random import randint


class FireVfx:
    def __init__(self, game):
        self.game = game
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pygame.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT], pygame.SRCALPHA)

    def do_fire(self):
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rnd = randint(0, 3)
                    self.fire_array[y - 1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    self.fire_array[y - 1][x] = 0

    def draw_fire(self):
        self.fire_surf.fill((0, 0, 0, 0))
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE,
                                                   PIXEL_SIZE, PIXEL_SIZE), color)

        for i in range(FIRE_REPS):
            self.game.display.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))

    def get_fire_array(self):
        fire_array = [[0 for i in range(FIRE_WIDTH)] for j in range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH):
            fire_array[FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return fire_array

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                c = pygame.Color(c1).lerp(c2, (step + 0.5) / STEPS_BETWEEN_COLORS)
                palette.append(c)

        return palette

    def update(self):
        self.do_fire()

    def draw(self):
        self.draw_fire()
