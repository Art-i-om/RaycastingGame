import pygame
from array import array
import moderngl


class GLRenderer:
    def __init__(self, game, ctx):
        self.game = game
        self.ctx = ctx
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,  # Top-left
            1.0, 1.0, 1.0, 0.0,  # Top-right
            -1.0, -1.0, 0.0, 1.0,  # Bottom-left
            1.0, -1.0, 1.0, 1.0  # Bottom-right
        ]))
        with open('shaders/screen_vertex_shader.glsl', 'r') as vert_shader_file:
            screen_vertex_shader = vert_shader_file.read()
        with open('shaders/screen_fragment_shader.glsl', 'r') as frag_shader_file:
            screen_fragment_shader = frag_shader_file.read()
        self.program = self.ctx.program(vertex_shader=screen_vertex_shader,
                                        fragment_shader=screen_fragment_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])
        self.frame_texture = self.create_texture(self.game.display)

    def create_texture(self, surface: pygame.Surface):
        texture = self.ctx.texture(surface.get_size(), 4)
        texture.filter = (moderngl.NEAREST, moderngl.LINEAR) # maybe change NEAREST later
        texture.swizzle = 'BGRA'
        return texture

    def apply_texture(self, surface: pygame.Surface):
        self.frame_texture.write(surface.get_view('1'))
        self.frame_texture.use(0)
        self.program['tex'] = 0
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
