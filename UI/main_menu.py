import pygame

from UI.fire_vfx import FireVfx
from settings import *
from UI.button import RectButton
import sys


class MainMenu:
    def __init__(self, game_flow, font_size = 40, logo_font_size = 200, main_font ='resources/fonts/RetroBanker.ttf'):
        self.game_flow = game_flow
        self.font = pygame.font.Font(main_font, font_size)
        self.logo_font = pygame.font.Font(main_font, logo_font_size)
        self.start_btn = RectButton(text="Start Game", pos=(HALF_WIDTH - 150, HALF_HEIGHT - 100),
                                    size=(300, 60), font=self.font,
                                    bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100))
        self.quit_btn = RectButton(text="Quit", pos=(HALF_WIDTH - 150, HALF_HEIGHT + 100),
                                   size=(300, 60), font=self.font,
                                   bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100))
        self.level_editor_btn = RectButton(text="Level Editor", pos=(HALF_WIDTH - 150, HALF_HEIGHT),
                                   size=(300, 60), font=self.font,
                                   bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100))
        self.logo = self.logo_font.render("DOOMED", False, (255, 0, 0)).convert_alpha()
        self.logo_x, self.logo_y = (WIDTH // 2 - self.logo.get_width() // 2,
                                    HEIGHT // 4 - self.logo.get_height() // 2)
        self.start_logo_y = HEIGHT
        self.logo_surf = pygame.Surface([WIDTH, HEIGHT])
        self.fire_vfx = None
        self.running = True

    def draw_logo(self):
        self.logo_surf.fill((0, 0, 0, 0))
        if self.start_logo_y > self.logo_y:
            self.start_logo_y -= 4
        self.logo_surf.blit(self.logo, (self.logo_x, self.start_logo_y))
        self.game_flow.display.blit(self.logo_surf, (0, 0))

    def check_events(self):
        for event in pygame.event.get():
            if self.start_btn.is_clicked(event):
                self.running = False
                self.game_flow.level_selector.run()
            if self.level_editor_btn.is_clicked(event):
                self.running = False
                self.game_flow.to_level_editor()
            if self.quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

    def update(self):
        self.fire_vfx.update()

    def draw(self):
        self.draw_logo()

        self.fire_vfx.draw()

        self.start_btn.draw(self.game_flow.display)
        self.level_editor_btn.draw(self.game_flow.display)
        self.quit_btn.draw(self.game_flow.display)

        self.game_flow.gl_renderer.apply_texture(self.game_flow.display)

        pygame.display.flip()

    def run(self):
        self.running = True
        self.start_logo_y = HEIGHT
        self.fire_vfx = FireVfx(self.game_flow)
        pygame.mouse.set_visible(True)
        self.game_flow.sound.play_main_menu_music()
        while self.running:
            self.check_events()
            self.update()
            self.draw()