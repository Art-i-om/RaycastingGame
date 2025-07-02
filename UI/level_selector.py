import sys
import os
import pygame
import tkinter as tk
from tkinter import filedialog
from settings import *
from UI.button import RectButton
from UI.scroll_view import ScrollView


class LevelSelectorMenu:
    def __init__(self, game_flow):
        self.game_flow = game_flow
        self.font = pygame.font.Font('resources/fonts/RetroBanker.ttf', 40)
        self.running = True

        map_files = sorted([f for f in os.listdir('maps') if f.endswith('.csv')])

        self.scroll_view = ScrollView(pos=(HALF_WIDTH - 250, 100), size=(500, HEIGHT - 350),
                                      items=map_files, item_height=60,
                                      font=pygame.font.Font('resources/fonts/RetroBanker.ttf', 30))

        self.load_file_btn = RectButton(pos=(HALF_WIDTH - 150, HEIGHT - 200), size=(300, 60),
                                        font=self.font, text='Load level',
                                        bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100)
                                        )
        self.back_button = RectButton(pos=(HALF_WIDTH - 150, HEIGHT - 120), size=(300, 60),
                                      font=self.font, text='Back',
                                      bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100)
                                      )

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            scroll_event = self.scroll_view.handle_event(event)
            if scroll_event and scroll_event['type'] == 'item_clicked':
                selected_map = scroll_event['item']
                self.load_premade_level(selected_map)

            if self.load_file_btn.is_clicked(event):
                self.load_csv_level()

            if self.back_button.is_clicked(event):
                self.running = False
                self.game_flow.to_main_menu()

    def run(self):
        self.running = True
        self.scroll_view.items = sorted([f[:-4] for f in os.listdir('maps') if f.endswith('.csv')])
        pygame.mouse.set_visible(True)
        while self.running:
            self.check_events()
            self.draw()

    def draw(self):
        self.game_flow.display.fill((0, 0, 0))
        self.scroll_view.draw(self.game_flow.display)
        self.load_file_btn.draw(self.game_flow.display)
        self.back_button.draw(self.game_flow.display)

        self.game_flow.gl_renderer.apply_texture(self.game_flow.display)

        pygame.display.flip()

    def load_premade_level(self, map_file):
        self.running = False
        self.game_flow.load_level(f"maps/{map_file}.csv")

    def load_csv_level(self):
        tk.Tk().withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")],
                                               title="Open Level")
        if file_path:
            self.running = False
            self.game_flow.load_level(file_path)
