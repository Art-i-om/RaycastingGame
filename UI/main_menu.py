import pygame
from settings import *
from UI.button import Button
import sys


class MainMenu:
    def __init__(self, game, font_size = 40, logo_font_size = 200, main_font ='resources/fonts/RetroBanker.ttf'):
        self.game = game
        self.game.sound.play_main_menu_music()
        self.font = pygame.font.Font(main_font, font_size)
        self.logo_font = pygame.font.Font(main_font, logo_font_size)
        self.start_btn = Button("Start Game", (HALF_WIDTH - 150, HALF_HEIGHT - 100), (300, 60), self.font,
                           bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100))
        self.quit_btn = Button("Quit", (HALF_WIDTH - 150, HALF_HEIGHT), (300, 60), self.font,
                          bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(100, 100, 100))
        self.logo = self.logo_font.render("DOOMED", False, (255, 0, 0)).convert_alpha()
        self.logo_x, self.logo_y = (WIDTH // 2 - self.logo.get_width() // 2,
                                    HEIGHT // 4 - self.logo.get_height() // 2)
        self.start_logo_y = HEIGHT
        self.logo_surf = pygame.Surface([WIDTH, HEIGHT])
        self.running = True

    def draw_logo(self):
        self.logo_surf.fill((0, 0, 0, 0))
        if self.start_logo_y > self.logo_y:
            self.start_logo_y -= 4
        self.logo_surf.blit(self.logo, (self.logo_x, self.start_logo_y))
        self.game.screen.blit(self.logo_surf, (0, 0))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.start_btn.is_clicked(event):
                self.game.new_game()
                pygame.mouse.set_visible(False)
                self.running = False
            if self.quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

    def update(self):
        self.game.fire_vfx.update()

    def draw(self):
        self.draw_logo()

        self.game.fire_vfx.draw()

        self.start_btn.draw(self.game.screen)
        self.quit_btn.draw(self.game.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()