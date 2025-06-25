from sprite_object import *
from npc import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = {}
        self.load_sprites_from_map(self.game.map.sprite_positions, self.game.map.npc_positions)

    def load_sprites_from_map(self, sprite_positions, npc_positions):
        for pos, sprite_id in sprite_positions:
            if sprite_id == 4:
                self.add_sprite(SpriteObject(self.game, pos=pos))
            elif sprite_id == 5:
                self.add_sprite(AnimatedSprite(self.game, pos=pos))

        for pos, sprite_id in npc_positions:
            if sprite_id == 6:
                self.add_npc(Soldier(self.game, pos=pos))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
