import pygame


class Button:
    def __init__(self, text, pos, size, font, bg_color, text_color, hover_color):
        self.rect = pygame.Rect(pos, size)
        self.font = font
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.rect, 2)  # border

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(pygame.mouse.get_pos())
