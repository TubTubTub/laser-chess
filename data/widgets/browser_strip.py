import pygame
from data.widgets.bases import _Widget
from data.widgets.browser_item import BrowserItem
from data.constants import BrowserEventType
from data.components.custom_event import CustomEvent

WIDTH_FACTOR = 0.3

class BrowserStrip(_Widget):
    def __init__(self, relative_height, games_list, **kwargs):
        super().__init__(relative_size=None, **kwargs)
        self._relative_item_width = relative_height / 2
        self._get_rect = None

        self._games_list = []
        self._items_list = []
        self._selected_index = None

        self.initialise_games_list(games_list)

    @property
    def item_width(self):
        return self._relative_item_width * self.surface_size[1]

    @property
    def size(self):
        if self._get_rect:
            height = self._get_rect().height
        else:
            height = 0
        width = max(0, len(self._games_list) * (self.item_width + self.margin) + self.margin)

        return (width, height)
    
    def register_get_rect(self, get_rect_func):
        self._get_rect = get_rect_func

    def initialise_games_list(self, games_list):
        self._items_list = []
        self._games_list = games_list
        self._selected_index = None

        for game in games_list:
            browser_item = BrowserItem(relative_position=(0, 0), game=game, relative_width=self._relative_item_width)
            self._items_list.append(browser_item)

        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        for index, item in enumerate(self._items_list):
            item.set_image()
            browser_item_position = (index * (self.item_width + self.margin) + self.margin, self.margin)
            self.image.blit(item.image, browser_item_position)

        if self._selected_index is not None:
            border_position = (self._selected_index * (self.item_width + self.margin), 0)
            border_size = (self.item_width + 2 * self.margin, self.size[1])
            pygame.draw.rect(self.image, (255, 255, 255), (*border_position, *border_size), width=int(self.item_width / 20))
    
    def set_geometry(self):
        super().set_geometry()
        for item in self._items_list:
            item.set_geometry()
    
    def set_surface_size(self, new_surface_size):
        super().set_surface_size(new_surface_size)
        for item in self._items_list:
            item.set_surface_size(new_surface_size)
    
    def process_event(self, event, scrolled_pos):
        parent_pos = self._get_rect().topleft
        self.rect.topleft = parent_pos

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._selected_index = None
            self.set_image()
            return CustomEvent(BrowserEventType.BROWSER_STRIP_CLICK, selected_index=None)
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            relative_mouse_pos = (event.pos[0] - parent_pos[0], event.pos[1] - parent_pos[1])
            self._selected_index = int(max(0, (relative_mouse_pos[0] - self.margin) // (self.item_width + self.margin)))
            self.set_image()
            return CustomEvent(BrowserEventType.BROWSER_STRIP_CLICK, selected_index=self._selected_index)