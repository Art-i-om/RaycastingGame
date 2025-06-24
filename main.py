import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from UI.main_menu import *
from UI.fire_vfx import *


class Game:
    def __init__(self, game_flow):
        self.game_flow = game_flow
        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40)
        self.screen = game_flow.screen
        self.delta_time = game_flow.delta_time
        self.clock = game_flow.clock
        self.sound = game_flow.sound
        self.map = None
        self.player = None
        self.raycasting = None
        self.object_renderer = None
        self.object_handler = None
        self.weapon = None
        self.pathfinding = None

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.delta_time = self.clock.tick(FPS)

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()
        pygame.display.flip()

    def check_events(self):
        self.global_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        pygame.mouse.set_visible(False)
        self.game_flow.sound.play_game_music()
        while True:
            self.check_events()
            self.update()
            self.draw()
