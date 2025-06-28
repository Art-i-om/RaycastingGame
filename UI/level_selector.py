import sys

import pygame
import tkinter as tk
from tkinter import filedialog
from settings import *
from UI.button import RectButton

class LevelSelectorMenu:
    def __init__(self, game_flow):
        self.game_flow = game_flow
        self.font = pygame.font.Font('resources/fonts/RetroBanker.ttf', 40)
        self.running = True

        self.levels_count = 2
        self.level_buttons = []
        for i in range(self.levels_count):
            level_button = RectButton(pos=(HALF_WIDTH - 150, HALF_HEIGHT - 200 + (60 * i)), size=(300, 60),
                                      font=self.font, text=f'Level {i + 1}',
                                      bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100)
            )
            self.level_buttons.append(level_button)


        self.load_file_btn = RectButton(pos=(HALF_WIDTH - 150, HEIGHT - 300), size=(300, 60),
                                        font=self.font, text='Load level',
                                        bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100)
        )

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            for i, button in enumerate(self.level_buttons):
                if button.is_clicked(event):
                    self.load_premade_level(i)

            if self.load_file_btn.is_clicked(event):
                self.load_csv_level()

    def run(self):
        pygame.mouse.set_visible(True)
        while self.running:
            self.check_events()
            self.draw()

    def draw(self):
        self.game_flow.display.fill((0, 0, 0))
        for button in self.level_buttons:
            button.draw(self.game_flow.display)
        self.load_file_btn.draw(self.game_flow.display)
        pygame.display.flip()

    def load_premade_level(self, index):
        self.running = False
        self.game_flow.load_level(f"maps/Level{index + 1}.csv")

    def load_csv_level(self):
        tk.Tk().withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")],
                                               title="Open Level")
        if file_path:
            self.running = False
            self.game_flow.load_level(file_path)
