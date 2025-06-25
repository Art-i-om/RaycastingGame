from UI.level_selector import LevelSelectorMenu
from game import *
from settings import *


class GameFlow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.file_path = None
        self.game = None
        self.fire_vfx = None
        self.sound = None
        self.main_menu = None
        self.level_selector = None
        self.awake_setup()

    def awake_setup(self):
        self.fire_vfx = FireVfx(self)
        self.sound = Sound(self)
        self.level_selector = LevelSelectorMenu(self)
        self.main_menu = MainMenu(self)
        self.game = Game(self)

    def play(self):
        self.game.run()

    def to_main_menu(self):
        self.main_menu.run()

    def to_level_selector(self):
        self.level_selector.run()

    def load_level(self, filepath):
        self.file_path = filepath
        self.game.new_game(self.file_path)
        self.play()


if __name__ == '__main__':
    game_flow = GameFlow()
    game_flow.to_main_menu()
