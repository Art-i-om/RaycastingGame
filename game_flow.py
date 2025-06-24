import pygame
from UI.fire_vfx import *
from sound import *
from UI.main_menu import *
from main import *
from settings import *


class GameFlow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.game = None
        self.fire_vfx = None
        self.sound = None
        self.main_menu = None
        self.running_game = False
        self.in_main_menu = True
        self.awake_setup()

    def awake_setup(self):
        self.fire_vfx = FireVfx(self)
        self.sound = Sound(self)
        self.main_menu = MainMenu(self)
        self.game = Game(self)

    def change_game_state(self):
        self.in_main_menu = not self.in_main_menu
        self.running_game = not self.running_game

    def run(self):
        if self.in_main_menu:
            self.main_menu.run()
        elif self.running_game:
            self.game.new_game()
            self.game.run()

if __name__ == '__main__':
    game_flow = GameFlow()
    game_flow.run()
