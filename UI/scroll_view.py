import pygame
from settings import *


class ScrollView:
    def __init__(self, pos, size, items=None, item_height=60, font=None,
                 bg_color=(30, 30, 30), item_bg_color=(50, 50, 50),
                 item_hover_color=(100, 100, 100), text_color=(255, 255, 255),
                 scroll_bar_color=(150, 150, 150), scroll_thumb_color=(200, 200, 200)):

        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.items = items or []
        self.item_height = item_height
        self.font = font or pygame.font.Font('resources/fonts/RetroBanker.ttf', 30)

        # Colors
        self.bg_color = bg_color
        self.item_bg_color = item_bg_color
        self.item_hover_color = item_hover_color
        self.text_color = text_color
        self.scroll_bar_color = scroll_bar_color
        self.scroll_thumb_color = scroll_thumb_color

        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = 0
        self.visible_items = self.size[1] // item_height
        self.scroll_speed = 30

        # Scroll bar
        self.scroll_bar_width = 20
        self.scroll_bar_rect = pygame.Rect(
            self.pos[0] + self.size[0] - self.scroll_bar_width,
            self.pos[1],
            self.scroll_bar_width,
            self.size[1]
        )

        # Selection
        self.selected_index = -1
        self.hovered_index = -1

        # Scrollbar dragging
        self.dragging_scrollbar = False
        self.drag_start_y = 0
        self.drag_start_scroll = 0

        self.update_scroll_limits()

    def set_items(self, items):
        self.items = items or []
        self.scroll_offset = 0
        self.selected_index = -1
        self.update_scroll_limits()

    def add_item(self, item):
        self.items.append(item)
        self.update_scroll_limits()

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            if self.selected_index >= index:
                self.selected_index = max(-1, self.selected_index - 1)
            self.update_scroll_limits()

    def clear_items(self):
        self.items = []
        self.scroll_offset = 0
        self.selected_index = -1
        self.update_scroll_limits()

    def update_scroll_limits(self):
        total_height = len(self.items) * self.item_height
        self.max_scroll = max(0, total_height - self.size[1])
        self.scroll_offset = min(self.scroll_offset, self.max_scroll)

    def get_scroll_thumb_rect(self):
        if self.max_scroll == 0:
            return pygame.Rect(0, 0, 0, 0)

        thumb_height = max(20, (self.size[1] / (len(self.items) * self.item_height)) * self.size[1])
        thumb_y = self.pos[1] + (self.scroll_offset / self.max_scroll) * (self.size[1] - thumb_height)

        return pygame.Rect(
            self.scroll_bar_rect.x,
            thumb_y,
            self.scroll_bar_width,
            thumb_height
        )

    def handle_event(self, event):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered_index = -1
            return None

        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            thumb_rect = self.get_scroll_thumb_rect()
            if thumb_rect.collidepoint(mouse_pos):
                self.dragging_scrollbar = True
                self.drag_start_y = mouse_pos[1]
                self.drag_start_scroll = self.scroll_offset
                return None

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
            delta_y = mouse_pos[1] - self.drag_start_y
            if self.max_scroll > 0:
                scroll_ratio = delta_y / (self.size[1] - self.get_scroll_thumb_rect().height)
                self.scroll_offset = max(0, min(self.max_scroll,
                                              self.drag_start_scroll + scroll_ratio * self.max_scroll))
            return None

        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(self.max_scroll,
                                          self.scroll_offset - event.y * self.scroll_speed))
            return None

        relative_x = mouse_pos[0] - self.pos[0]
        relative_y = mouse_pos[1] - self.pos[1] + self.scroll_offset

        if 0 <= relative_x < self.size[0] - self.scroll_bar_width:
            item_index = int(relative_y // self.item_height)

            if 0 <= item_index < len(self.items):
                self.hovered_index = item_index

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.selected_index = item_index
                    return {'type': 'item_clicked', 'index': item_index, 'item': self.items[item_index]}

        return None

    def get_selected_item(self):
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None

    def get_selected_index(self):
        return self.selected_index if 0 <= self.selected_index < len(self.items) else -1

    def set_selected_index(self, index):
        if 0 <= index < len(self.items):
            self.selected_index = index
            item_y = index * self.item_height
            if item_y < self.scroll_offset:
                self.scroll_offset = item_y
            elif item_y + self.item_height > self.scroll_offset + self.size[1]:
                self.scroll_offset = item_y + self.item_height - self.size[1]
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
        else:
            self.selected_index = -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)

        clip_rect = pygame.Rect(self.pos[0], self.pos[1],
                               self.size[0] - self.scroll_bar_width, self.size[1])
        screen.set_clip(clip_rect)

        start_index = max(0, int(self.scroll_offset // self.item_height))
        end_index = min(len(self.items), start_index + self.visible_items + 2)

        for i in range(start_index, end_index):
            item_y = self.pos[1] + i * self.item_height - self.scroll_offset
            item_rect = pygame.Rect(self.pos[0], item_y,
                                   self.size[0] - self.scroll_bar_width, self.item_height)

            if item_y + self.item_height < self.pos[1] or item_y > self.pos[1] + self.size[1]:
                continue

            if i == self.selected_index:
                bg_color = self.item_hover_color
            elif i == self.hovered_index:
                bg_color = tuple(min(255, c + 20) for c in self.item_bg_color)
            else:
                bg_color = self.item_bg_color

            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(screen, (70, 70, 70), item_rect, 1)

            text = str(self.items[i])
            text_surf = self.font.render(text, True, self.text_color)
            text_x = item_rect.x + 10
            text_y = item_rect.y + (self.item_height - text_surf.get_height()) // 2
            screen.blit(text_surf, (text_x, text_y))

        screen.set_clip(None)

        if len(self.items) * self.item_height > self.size[1]:
            pygame.draw.rect(screen, self.scroll_bar_color, self.scroll_bar_rect)
            thumb_rect = self.get_scroll_thumb_rect()
            pygame.draw.rect(screen, self.scroll_thumb_color, thumb_rect)
