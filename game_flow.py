import pygame

from UI.level_selector import LevelSelectorMenu
from UI.game_over import GameOverMenu
from level_editor import LevelEditor
from game import *
from settings import *
import moderngl


class GameFlow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES, pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface(self.screen.get_size())
        self.ctx = moderngl.create_context()
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.gl_renderer = None
        self.file_path = None
        self.game = None
        self.sound = None
        self.main_menu = None
        self.level_selector = None
        self.game_over = None
        self.level_editor = None
        self.awake_setup()

    def awake_setup(self):
        self.sound = Sound(self)
        self.level_selector = LevelSelectorMenu(self)
        self.main_menu = MainMenu(self)
        self.game_over = GameOverMenu(self)
        self.level_editor = LevelEditor(self)
        self.game = Game(self)
        self.gl_renderer = GLRenderer(self.game, self.ctx)

    def play(self):
        self.game.run()

    def to_game_over_menu(self):
        self.game_over.run()

    def to_main_menu(self):
        self.main_menu.run()

    def to_level_selector(self):
        self.level_selector.run()

    def to_level_editor(self):
        self.level_editor.run()

    def load_level(self, filepath):
        self.file_path = filepath
        self.game.new_game(self.file_path)
        self.play()


if __name__ == '__main__':
    game_flow = GameFlow()
    game_flow.to_main_menu()
