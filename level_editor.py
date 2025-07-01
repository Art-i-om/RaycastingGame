import csv
import sys
import os
import pygame
import tkinter
from tkinter import filedialog
from UI.button import ImageButton, RectButton
from settings import *


class LevelEditor:
    def __init__(self, game_flow):
        self.game_flow = game_flow
        self.display = game_flow.display
        self.running = True
        self.delta_time = 1
        self.current_tile = 1
        self.player_placed = False
        self.root = tkinter.Tk()
        self.root.withdraw()
        self.clock = game_flow.clock
        self.level_name = None
        self.scroll_left = False
        self.scroll_right = False
        self.scroll_down = False
        self.scroll_up = False
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_speed = 5
        self.scroll_speed_multiplier = 1
        self.sky_image = pygame.image.load('resources/textures/level_editor_background.png').convert_alpha()
        self.tile_list = [None]
        for x in range(1, TILE_TYPES + 1):
            img = pygame.image.load(f'resources/tilemap_editor/{x}.png').convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.tile_list.append(img)
        self.world_data = []
        for row in range(MAX_ROWS):
            r = [0] * MAX_COLS
            self.world_data.append(r)
        self.save_button = RectButton(
            (EDITOR_WIDTH - 250, EDITOR_HEIGHT + LOWER_MARGIN - 75),
            (100, 50),
            "Save",
            bg_color=DEEP_RED,
            hover_color=BRIGHT_RED,
            text_color=WHITE
        )
        self.load_button = RectButton(
            (EDITOR_WIDTH - 100, EDITOR_HEIGHT + LOWER_MARGIN - 75),
            (100, 50),
            "Load",
            bg_color=DEEP_RED,
            hover_color=BRIGHT_RED,
            text_color=WHITE
        )
        self.exit_button = RectButton(
            (EDITOR_WIDTH + 150, EDITOR_HEIGHT + LOWER_MARGIN - 75),
            (100, 50),
            "Exit",
            bg_color=DEEP_RED,
            hover_color=BRIGHT_RED,
            text_color=WHITE
        )
        self.button_list = []
        self.button_col = 0
        self.button_row = 0
        for i in range(1, len(self.tile_list)):
            img = self.tile_list[i]
            tile_button = ImageButton(pos=(EDITOR_WIDTH + (75 * self.button_col) + 50, 75 * self.button_row + 50),
                                      size=(img.get_width(), img.get_height()), image=img)
            self.button_list.append(tile_button)
            self.button_col += 1
            if self.button_col == 3:
                self.button_row += 1
                self.button_col = 0

    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile > 0:
                    self.display.blit(self.tile_list[tile], (x * TILE_SIZE - self.scroll_x, y * TILE_SIZE - self.scroll_y))

    def draw_grid(self):
        for c in range(MAX_COLS + 1):
            pygame.draw.line(self.display, WHITE, (c * TILE_SIZE - self.scroll_x, 0), (c * TILE_SIZE - self.scroll_x, EDITOR_HEIGHT))

        for r in range(MAX_ROWS + 1):
            pygame.draw.line(self.display, WHITE, (0, r * TILE_SIZE - self.scroll_y), (EDITOR_WIDTH, r * TILE_SIZE - self.scroll_y))

    def draw_background(self):
        self.display.fill(DARK_RED)
        width = self.sky_image.get_width()
        height = self.sky_image.get_height()
        for y in range(5):
            for x in range(6):
                self.display.blit(self.sky_image, ((x * width) - self.scroll_x, (y * height) - self.scroll_y))

    def draw_text(self, text, text_col, x, y, font=None):
        font = font or pygame.font.Font('resources/fonts/RetroBanker.ttf', 40)
        img = font.render(text, True, text_col)
        self.display.blit(img, (x, y))

    def scroll(self):
        if self.scroll_left and self.scroll_x > 0:
            self.scroll_x -= self.scroll_speed * self.scroll_speed_multiplier
        if self.scroll_right and self.scroll_x < (MAX_COLS * TILE_SIZE) - EDITOR_WIDTH:
            self.scroll_x += self.scroll_speed * self.scroll_speed_multiplier
        if self.scroll_up and self.scroll_y > 0:
            self.scroll_y -= self.scroll_speed * self.scroll_speed_multiplier
        if self.scroll_down and self.scroll_y < (MAX_ROWS * TILE_SIZE) - EDITOR_HEIGHT:
            self.scroll_y += self.scroll_speed * self.scroll_speed_multiplier

        if self.scroll_x < 0:
            self.scroll_x = 0
        if self.scroll_x > (MAX_COLS * TILE_SIZE) - EDITOR_WIDTH:
            self.scroll_x = (MAX_COLS * TILE_SIZE) - EDITOR_WIDTH
        if self.scroll_y < 0:
            self.scroll_y = 0
        if self.scroll_y > (MAX_ROWS * TILE_SIZE) - EDITOR_HEIGHT:
            self.scroll_y = (MAX_ROWS * TILE_SIZE) - EDITOR_HEIGHT

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.scroll_left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.scroll_right = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.scroll_up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.scroll_down = True
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.scroll_speed_multiplier = 4

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.scroll_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.scroll_right = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.scroll_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.scroll_down = False
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.scroll_speed_multiplier = 1

            for button_count, button in enumerate(self.button_list):
                if button.is_clicked(event):
                    self.current_tile = button_count + 1

            if self.save_button.is_clicked(event):
                file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                        filetypes=[("Level Files", "*.csv"), ("All Files", "*.*")],
                                                        title="Save Level As")

                if file_path:
                    with open(file_path, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=' ')
                        for row in self.world_data:
                            writer.writerow(row)

            if self.load_button.is_clicked(event):
                file_path = filedialog.askopenfilename(defaultextension=".csv",
                                                       filetypes=[("Level Files", "*.csv"), ("All Files", "*.*")],
                                                       title="Open Level")

                if file_path:
                    scroll_x, scroll_y = 0, 0
                    with open(file_path, newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=' ')
                        loaded_data = []
                        for row in reader:
                            loaded_data.append([int(tile) for tile in row])

                        world_data = loaded_data

                        level_name = os.path.splitext(os.path.basename(file_path))[0]

            if self.exit_button.is_clicked(event):
                self.running = False
                self.game_flow.to_main_menu()

        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] + self.scroll_x) // TILE_SIZE
        y = (mouse_pos[1] + self.scroll_y) // TILE_SIZE

        if mouse_pos[0] < EDITOR_WIDTH and mouse_pos[1] < EDITOR_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if self.current_tile == 1:
                    if not self.player_placed and self.world_data[y][x] != 1:
                        self.world_data[y][x] = 1
                        self.player_placed = True
                else:
                    if self.world_data[y][x] != self.current_tile:
                        self.world_data[y][x] = self.current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                if self.player_placed and self.world_data[y][x] == 1:
                    self.player_placed = False
                self.world_data[y][x] = 0

    def update(self):
        self.scroll()

        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.draw_background()
        self.draw_grid()
        self.draw_world()

        pygame.draw.rect(self.display, DEEP_RED, (0, EDITOR_HEIGHT, EDITOR_WIDTH + SIDE_MARGIN, LOWER_MARGIN))
        self.save_button.draw(self.display)
        self.load_button.draw(self.display)
        self.exit_button.draw(self.display)

        pygame.draw.rect(self.display, DARK_RED, (EDITOR_WIDTH, 0, SIDE_MARGIN, EDITOR_HEIGHT))
        self.draw_text(f'Level name: {self.level_name}', WHITE, 10, EDITOR_HEIGHT + LOWER_MARGIN - 90)

        for button in self.button_list:
            button.draw(self.display)

        pygame.draw.rect(self.display, BRIGHT_RED, self.button_list[self.current_tile - 1].rect, 3)

        self.game_flow.gl_renderer.apply_texture(self.display)

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()
