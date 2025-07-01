import csv
import sys
import os
import pygame
import tkinter
from tkinter import filedialog
from UI.button import ImageButton, RectButton

pygame.init()
root = tkinter.Tk()
root.withdraw()

clock = pygame.time.Clock()
FPS = 200

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

MAX_ROWS = 150
MAX_COLS = 150
TILE_SIZE = 32
TILE_TYPES = 7
current_tile = 1
player_placed = False

level_name = 'test name'
scroll_left = False
scroll_right = False
scroll_down = False
scroll_up = False
scroll_x = 0
scroll_y = 0
scroll_speed = 5
scroll_speed_multiplier = 1

sky_image = pygame.image.load('resources/textures/level_editor_background.png').convert_alpha()

tile_list = [None]
for x in range(1, TILE_TYPES + 1):
    img = pygame.image.load(f'resources/tilemap_editor/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_list.append(img)

DARK_RED = (80, 0, 0)
BRIGHT_RED = (200, 30, 30)
DEEP_RED = (150, 0, 0)
LIGHT_RED = (255, 100, 100)
WHITE = (255, 255, 255)

world_data = []
for row in range(MAX_ROWS):
    r = [0] * MAX_COLS
    world_data.append(r)


def draw_text(text, text_col, x, y, font=None):
    font = font or pygame.font.Font('resources/fonts/RetroBanker.ttf', 40)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_background():
    screen.fill(DARK_RED)
    width = sky_image.get_width()
    height = sky_image.get_height()
    for y in range(5):
        for x in range(6):
            screen.blit(sky_image, ((x * width) - scroll_x, (y * height) - scroll_y))


def draw_grid():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll_x, 0), (c * TILE_SIZE - scroll_x, SCREEN_HEIGHT))

    for r in range(MAX_ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, r * TILE_SIZE - scroll_y), (SCREEN_WIDTH, r * TILE_SIZE - scroll_y))


def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile > 0:
                screen.blit(tile_list[tile], (x * TILE_SIZE - scroll_x, y * TILE_SIZE - scroll_y))


save_button = RectButton(
    (SCREEN_WIDTH - 250, SCREEN_HEIGHT + LOWER_MARGIN - 75),
    (100, 50),
    "Save",
    bg_color=DEEP_RED,
    hover_color=BRIGHT_RED,
    text_color=WHITE
)
load_button = RectButton(
    (SCREEN_WIDTH - 100, SCREEN_HEIGHT + LOWER_MARGIN - 75),
    (100, 50),
    "Load",
    bg_color=DEEP_RED,
    hover_color=BRIGHT_RED,
    text_color=WHITE
)

button_list = []
button_col = 0
button_row = 0
for i in range(1, len(tile_list)):
    img = tile_list[i]
    tile_button = ImageButton(pos=(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50),
                         size=(img.get_width(), img.get_height()), image=img)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

running = True
while running:

    clock.tick(FPS)
    pygame.display.set_caption(f'{clock.get_fps() :.1f}')

    if scroll_left and scroll_x > 0:
        scroll_x -= scroll_speed * scroll_speed_multiplier
    if scroll_right and scroll_x < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll_x += scroll_speed * scroll_speed_multiplier
    if scroll_up and scroll_y > 0:
        scroll_y -= scroll_speed * scroll_speed_multiplier
    if scroll_down and scroll_y < (MAX_ROWS * TILE_SIZE) - SCREEN_HEIGHT:
        scroll_y += scroll_speed * scroll_speed_multiplier

    if scroll_x < 0:
        scroll_x = 0
    if scroll_x > (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll_x = (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH
    if scroll_y < 0:
        scroll_y = 0
    if scroll_y > (MAX_ROWS * TILE_SIZE) - SCREEN_HEIGHT:
        scroll_y = (MAX_ROWS * TILE_SIZE) - SCREEN_HEIGHT

    mouse_pos = pygame.mouse.get_pos()
    x = (mouse_pos[0] + scroll_x) // TILE_SIZE
    y = (mouse_pos[1] + scroll_y) // TILE_SIZE

    if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if current_tile == 1:
                    if not player_placed and world_data[y][x] != 1:
                        world_data[y][x] = 1
                        player_placed = True
                else:
                    if world_data[y][x] != current_tile:
                        world_data[y][x] = current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                if player_placed and world_data[y][x] == 1:
                    player_placed = False
                world_data[y][x] = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                scroll_up = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                scroll_down = True
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed_multiplier = 4

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                scroll_up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                scroll_down = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed_multiplier = 1

        for button_count, button in enumerate(button_list):
            if button.is_clicked(event):
                current_tile = button_count + 1

        if save_button.is_clicked(event):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("Level Files", "*.csv"), ("All Files", "*.*")],
                                                     title="Save Level As")

            if file_path:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ')
                    for row in world_data:
                        writer.writerow(row)

        if load_button.is_clicked(event):
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

    draw_background()
    draw_grid()
    draw_world()

    pygame.draw.rect(screen, DEEP_RED, (0, SCREEN_HEIGHT, SCREEN_WIDTH + SIDE_MARGIN, LOWER_MARGIN))
    save_button.draw(screen)
    load_button.draw(screen)

    pygame.draw.rect(screen, DARK_RED, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    draw_text(f'Level name: {level_name}', WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)

    for button in button_list:
        button.draw(screen)

    pygame.draw.rect(screen, BRIGHT_RED, button_list[current_tile - 1].rect, 3)

    pygame.display.flip()


# class LevelEditor:
#     def __init__(self):
#         self.running = True
#         self.delta_time = 1
#
#     def check_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#
#     def update(self):
#         self.delta_time = clock.tick(FPS)
#
#     def draw(self):
#         pygame.display.flip()
#
#     def run(self):
#         self.running = True
#         while self.running:
#             self.check_events()
#             self.update()
#             self.draw()
