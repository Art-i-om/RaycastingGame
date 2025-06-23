import pygame
import math
import numpy as np
from numba import njit
from settings import *
from map import DEFAULT_MAP_PATH


@njit(cache=True)
def _calc_wall_data(proj_heights, height, half_height, texture_size):
    n = len(proj_heights)
    wall_pos_y = np.empty(n, dtype=np.int32)
    wall_heights = np.empty(n, dtype=np.int32)
    use_small = np.empty(n, dtype=np.bool_)
    for i in range(n):
        ph = proj_heights[i]
        if ph < height:
            wall_heights[i] = int(ph)
            wall_pos_y[i] = int(half_height - ph // 2)
            use_small[i] = True
        else:
            wall_heights[i] = int(texture_size * height / ph)
            wall_pos_y[i] = 0
            use_small[i] = False
    return wall_pos_y, wall_heights, use_small

@njit(fastmath=True)
def ray_casting_jit(ox, oy, player_angle, world_array):
    """Return arrays with ray casting results using numba JIT."""
    depths = np.empty(NUM_RAYS, dtype=np.float64)
    proj_heights = np.empty(NUM_RAYS, dtype=np.float64)
    textures = np.empty(NUM_RAYS, dtype=np.int32)
    offsets = np.empty(NUM_RAYS, dtype=np.float64)

    x_map = int(ox)
    y_map = int(oy)

    ray_angle = player_angle - HALF_FOV + 0.0001
    for ray in range(NUM_RAYS):
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        y_hor = y_map + 1 if sin_a > 0 else y_map - 1e-6
        dy = 1 if sin_a > 0 else -1
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        texture_hor = 1
        for i in range(MAX_DEPTH):
            tile_hor_x = int(x_hor)
            tile_hor_y = int(y_hor)
            if 0 <= tile_hor_x < world_array.shape[1] and 0 <= tile_hor_y < world_array.shape[0]:
                cell = world_array[tile_hor_y, tile_hor_x]
                if cell:
                    texture_hor = int(cell)
                    break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        x_vert = x_map + 1 if cos_a > 0 else x_map - 1e-6
        dx_vert = 1 if cos_a > 0 else -1
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx_vert / cos_a
        dy_vert = delta_depth * sin_a
        texture_vert = 1
        for i in range(MAX_DEPTH):
            tile_vert_x = int(x_vert)
            tile_vert_y = int(y_vert)
            if 0 <= tile_vert_x < world_array.shape[1] and 0 <= tile_vert_y < world_array.shape[0]:
                cell = world_array[tile_vert_y, tile_vert_x]
                if cell:
                    texture_vert = int(cell)
                    break
            x_vert += dx_vert
            y_vert += dy_vert
            depth_vert += delta_depth

        if depth_vert < depth_hor:
            depth = depth_vert
            texture = texture_vert
            off = y_vert % 1 if cos_a > 0 else (1 - y_vert % 1)
        else:
            depth = depth_hor
            texture = texture_hor
            off = (1 - x_hor % 1) if sin_a > 0 else x_hor % 1

        depth *= math.cos(player_angle - ray_angle)
        proj_height = SCREEN_DIST / (depth + 0.0001)

        depths[ray] = depth
        proj_heights[ray] = proj_height
        textures[ray] = texture
        offsets[ray] = off

        ray_angle += DELTA_ANGLE

    return depths, proj_heights, textures, offsets

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.game.map.load_from_file(DEFAULT_MAP_PATH)
        self.world_array = np.array(
            [[cell if cell else 0 for cell in row] for row in self.game.map.mini_map],
            dtype=np.int32
        )
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_draw(self):
        self.objects_to_render = []

        if not self.ray_casting_result:
            return

        data = np.array(self.ray_casting_result, dtype=np.float32)
        depths = data[:, 0]
        proj_heights = data[:, 1]
        textures = data[:, 2].astype(np.int32)
        offsets = data[:, 3]

        pos_y, slice_heights, is_small = _calc_wall_data(
            proj_heights, HEIGHT, HALF_HEIGHT, TEXTURE_SIZE
        )

        for ray in range(len(self.ray_casting_result)):
            texture = textures[ray]
            offset = offsets[ray]
            depth = depths[ray]
            if is_small[ray]:
                wall_column = self.textures[texture].subsurface(
                    int(offset * (TEXTURE_SIZE - SCALE)), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, int(slice_heights[ray])))
                wall_pos = (ray * SCALE, int(pos_y[ray]))
            else:
                wall_column = self.textures[texture].subsurface(
                    int(offset * (TEXTURE_SIZE - SCALE)),
                    HALF_TEXTURE_SIZE - int(slice_heights[ray]) // 2,
                    SCALE,
                    int(slice_heights[ray])
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        """Perform ray casting using the numba optimized function."""
        ox, oy = self.game.player.pos

        depths, proj_heights, textures, offsets = ray_casting_jit(
            ox, oy, self.game.player.angle, self.world_array
        )
        self.ray_casting_result = [
            (depths[i], proj_heights[i], int(textures[i]), offsets[i])
            for i in range(NUM_RAYS)
        ]

    def update(self):
        self.ray_cast()
        self.get_objects_to_draw()
