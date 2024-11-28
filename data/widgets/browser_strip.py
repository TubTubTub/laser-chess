import pygame
from data.widgets.bases import _Widget
from data.widgets.browser_item import BrowserItem
from data.constants import BrowserEventType
from data.components.custom_event import CustomEvent

class BrowserStrip(_Widget):
    def __init__(self, relative_position, item_width, games_list, margin=20):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        
        self._relative_position = relative_position
        self._relative_item_width = item_width / self._screen_size[1]
        self._relative_margin = margin / self._screen_size[1]

        self._get_rect = None

        self._games_list = []
        self._items_list = []
        self._selected_index = None

        self.initialise_games_list(games_list)

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _item_width(self):
        return self._relative_item_width * self._screen_size[1]

    @property
    def _size(self):
        if self._get_rect:
            height = self._get_rect().height
        else:
            height = 0
        width = max(0, len(self._games_list) * (self._item_width + self._margin) + self._margin)

        return (width, height)
    
    @property
    def _margin(self):
        return self._relative_margin * self._screen_size[1]
    
    def register_get_rect(self, get_rect_func):
        self._get_rect = get_rect_func

    def initialise_games_list(self, games_list):
        self._items_list = []
        self._games_list = games_list
        self._selected_index = None

        for game in games_list:
            browser_item = BrowserItem(relative_position=(0, 0), game=game, width=self._item_width)
            self._items_list.append(browser_item)

        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.Surface(self._size, pygame.SRCALPHA)
        for index, item in enumerate(self._items_list):
            item.set_image()
            browser_item_position = (index * (self._item_width + self._margin) + self._margin, self._margin)
            self.image.blit(item.image, browser_item_position)

        if self._selected_index is not None:
            border_position = (self._selected_index * (self._item_width + self._margin), 0)
            border_size = (self._item_width + 2 * self._margin, self._size[1])
            pygame.draw.rect(self.image, (255, 255, 255), (*border_position, *border_size), width=int(self._item_width / 20))
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
        for item in self._items_list:
            item.set_geometry()
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
        for item in self._items_list:
            item.set_screen_size(new_screen_size)
    
    def process_event(self, event, scrolled_pos):
        parent_pos = self._get_rect().topleft
        self.rect.topleft = parent_pos

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._selected_index = None
            self.set_image()
            return CustomEvent(BrowserEventType.BROWSER_STRIP_CLICK, selected_index=None)
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            relative_mouse_pos = (event.pos[0] - parent_pos[0], event.pos[1] - parent_pos[1])
            self._selected_index = int(max(0, (relative_mouse_pos[0] - self._margin) // (self._item_width + self._margin)))
            self.set_image()
            return CustomEvent(BrowserEventType.BROWSER_STRIP_CLICK, selected_index=self._selected_index)