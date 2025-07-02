from settings import *
from GL_renderer import *
import pygame


class ObjectRenderer:
    def __init__(self, game, ctx):
        self.ctx = ctx
        self.game = game
        self.gl_renderer = GLRenderer(game, ctx)
        self.wall_textures = self.load_wall_texture()
        self.sky_image_front = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_image_back = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 100
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)

        self.show_blood = False
        self.blood_end_time = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects()

        if self.show_blood:
            self.show_blood_screen()

        self.draw_player_health()
        self.fps_shower()
        self.draw_weapon()

        self.gl_renderer.apply_texture(self.game.display)

        pygame.display.flip()

    def draw_weapon(self):
        self.game.weapon.draw()

    def fps_shower(self):
        fps = self.game.clock.get_fps()
        fps_surface = pygame.font.SysFont(None, 128).render(f"{fps :.1f}", True, (255, 255, 255))
        self.game.display.blit(fps_surface, (WIDTH - 300, 0))

    def game_over(self):
        self.game.display.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        offset = 30
        for i, char in enumerate(health):
            self.game.display.blit(self.digits[char], (i * self.digit_size + offset, 0))
        self.game.display.blit(self.digits['10'], ((i + 1) * self.digit_size + offset, 0))

    def player_damage(self, duration=50.0):
        self.show_blood = True
        self.blood_end_time = pygame.time.get_ticks() + duration

    def show_blood_screen(self):
        self.game.display.blit(self.blood_screen, (0, 0))
        if pygame.time.get_ticks() > self.blood_end_time:
            self.show_blood = False
            self.game.display.fill((0, 0, 0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.game.display.blit(self.sky_image_front, (-self.sky_offset, 0))
        self.game.display.blit(self.sky_image_back, (-self.sky_offset + WIDTH, 0))

        pygame.draw.rect(self.game.display, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.game.display.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def load_wall_texture(self):
        return {
            2: self.get_texture('resources/textures/1.png'),
            3: self.get_texture('resources/textures/2.png'),
            4: self.get_texture('resources/textures/3.png')
        }
