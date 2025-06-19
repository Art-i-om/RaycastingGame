import pygame.transform

from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=4, animation_time=90):
        super().__init__(game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pygame.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 4, HEIGHT - self.images[0].get_height())

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        pass
