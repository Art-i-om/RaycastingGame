import pygame
from settings import *
from UI.button import RectButton
import sys


class GameOverMenu:
    def __init__(self, game_flow, font_size=40, main_font='resources/fonts/RetroBanker.ttf'):
        self.game_flow = game_flow
        self.font = pygame.font.Font(main_font, font_size)
        self.restart_btn = RectButton(text="Restart Game", pos=(HALF_WIDTH - 150, HALF_HEIGHT - 100),
                                      size=(300, 60), font=self.font,
                                      bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100))
        self.main_menu_btn = RectButton(text="Main Menu", pos=(HALF_WIDTH - 150, HALF_HEIGHT),
                                   size=(300, 60), font=self.font,
                                   bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100))
        self.running = True

    def check_events(self):
        for event in pygame.event.get():
            if self.restart_btn.is_clicked(event):
                self.game_flow.load_level(self.game_flow.file_path)
            if self.main_menu_btn.is_clicked(event):
                self.game_flow.to_main_menu()

    def update(self):
        pass

    def draw(self):
        self.game_flow.display.fill((0, 0, 0))
        self.restart_btn.draw(self.game_flow.display)
        self.main_menu_btn.draw(self.game_flow.display)

        self.game_flow.gl_renderer.apply_texture(self.game_flow.display)

        pygame.display.flip()

    def run(self):
        self.running = True
        pygame.mouse.set_visible(True)
        while self.running:
            self.check_events()
            self.update()
            self.draw()
