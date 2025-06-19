from sprite_object import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite

        add_sprite(SpriteObject(game, pos=(14.75, 1.25)))
        add_sprite(SpriteObject(game, pos=(14.75, 1.75)))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(14.75, 7.75)))

    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
