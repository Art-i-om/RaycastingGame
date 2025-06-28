import pygame


class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = pygame.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pygame.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pygame.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_attack = pygame.mixer.Sound(self.path + 'npc_attack.wav')
        self.player_pain = pygame.mixer.Sound(self.path + 'player_pain.wav')
        self.shotgun.set_volume(0.1)
        self.npc_pain.set_volume(0.1)
        self.npc_death.set_volume(0.1)
        self.npc_attack.set_volume(0.1)
        self.player_pain.set_volume(0.1)

    def play_game_music(self):
        pygame.mixer.music.load(self.path + 'game_theme.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def play_main_menu_music(self):
        pygame.mixer.music.load(self.path + 'main_menu_theme.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()