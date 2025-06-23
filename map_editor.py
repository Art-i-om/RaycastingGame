import pygame
import sys
from map import DEFAULT_MAP_PATH

TILE_SIZE = 100
ROWS = 9
COLS = 16

IMAGE_MAP = {
    0: (30, 30, 30),
    1: pygame.image.load('resources/textures/1.png'),
    2: pygame.image.load('resources/textures/2.png'),
    3: pygame.image.load('resources/textures/3.png'),
}

def load_map(path):
    data = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append([int(x) for x in line.replace(',', ' ').split()])
    except FileNotFoundError:
        data = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    return data

def save_map(data, path):
    with open(path, 'w') as f:
        for row in data:
            f.write(' '.join(str(x) for x in row) + '\n')


def main():
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption('Map Editor')
    clock = pygame.time.Clock()

    current_tile = 1
    grid = load_map(DEFAULT_MAP_PATH)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    current_tile = event.key - pygame.K_0
                elif event.key == pygame.K_s:
                    save_map(grid, DEFAULT_MAP_PATH)
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                cx = mx // TILE_SIZE
                cy = my // TILE_SIZE
                if 0 <= cx < COLS and 0 <= cy < ROWS:
                    grid[cy][cx] = current_tile

        screen.fill((0, 0, 0))
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                val = grid[y][x]
                image = IMAGE_MAP.get(val, (100, 100, 100))
                if val == 0:
                    pygame.draw.rect(screen, image, rect)

                elif val:
                    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                    screen.blit(image, rect)
                pygame.draw.rect(screen, (60, 60, 60), rect, 1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
