import pygame
from data.constants import WidgetState
from data.components.circular_linked_list import CircularLinkedList
from data.managers.audio import audio
from data.managers.theme import theme
from data.managers.window import window
from data.assets import SFX, FONTS, DEFAULT_FONT

DEFAULT_SURFACE_SIZE = window.screen.size
REQUIRED_KWARGS = ['relative_position', 'relative_size']
COUNT = 0

class _Widget(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        # global COUNT
        # print(COUNT, 'INITIALSING BASE _WIDGET', self.__class__.__qualname__, kwargs.get('relative_position'))
        # COUNT = COUNT + 1
        super().__init__()

        for required_kwarg in REQUIRED_KWARGS:
            if required_kwarg not in kwargs:
                raise KeyError(f'(_Widget.__init__) Required keyword "{required_kwarg}" not in base kwargs')
            
        self._relative_font_size = None # SET IN EACH WIDGET
        
        self._surface = None # SET IN WIDGET GROUP, AS NEED TO BE FETCHED EVERY CALL
        self._raw_surface_size = DEFAULT_SURFACE_SIZE

        self._parent = kwargs.get('parent')

        self._relative_position = kwargs.get('relative_position')
        self._relative_margin = theme['margin'] / self._raw_surface_size[1]
        self._relative_border_width = theme['borderWidth'] / self._raw_surface_size[1]
        self._relative_border_radius = theme['borderRadius'] / self._raw_surface_size[1]
        
        self._anchor_x = kwargs.get('anchor_x') or 'left'
        self._anchor_y = kwargs.get('anchor_y') or 'top'
        self._fixed_position = kwargs.get('fixed_position')

        self._border_colour = pygame.Color(theme['borderPrimary'])
        self._text_colour = pygame.Color(theme['textPrimary'])
        self._fill_colour = pygame.Color(theme['fillPrimary'])

        scale_mode = kwargs.get('scale_mode') or 'both' # Relative scale based on surface width and height
        if kwargs.get('relative_size'):
            match scale_mode:
                case 'height':
                    self._relative_size = kwargs.get('relative_size')
                case 'width':
                    self._relative_size = ((kwargs.get('relative_size')[0] * self.surface_size[0]) / self.surface_size[1], (kwargs.get('relative_size')[1] * self.surface_size[0]) / self.surface_size[1])
                case 'both':
                    self._relative_size = ((kwargs.get('relative_size')[0] * self.surface_size[0]) / self.surface_size[1], kwargs.get('relative_size')[1])
                case _:
                    raise ValueError('(_Widget.__init__) Unknown scale mode:', scale_mode)
        else:
            self._relative_size = (1, 1)
        
        # if self._relative_size[0] > 2 or self._relative_size[1] > 2:
        #     raise ValueError('(_Widget.__init__) Relative size must be less than 2', self._relative_size, self._parent.size)
        
        if 'margin' in kwargs:
            self._relative_margin = kwargs.get('margin') / self._raw_surface_size[1]

            if (self._relative_margin * 2) > min(self._relative_size[0], self._relative_size[1]):
                raise ValueError('(_Widget.__init__) Margin larger than specified size!')
        
        if 'border_width' in kwargs:
            self._relative_border_width = kwargs.get('border_width') / self._raw_surface_size[1]
        
        if 'border_radius' in kwargs:
            self._relative_border_radius = kwargs.get('border_radius') / self._raw_surface_size[1]
        
        if 'border_colour' in kwargs:
            self._border_colour = pygame.Color(kwargs.get('border_colour'))
        
        if 'fill_colour' in kwargs:
            self._fill_colour = pygame.Color(kwargs.get('fill_colour'))
        
        if 'text_colour' in kwargs:
            self._text_colour = pygame.Color(kwargs.get('text_colour'))
        
        if 'font' in kwargs:
            self._font = kwargs.get('font')
        else:
            self._font = DEFAULT_FONT
    
    @property
    def surface_size(self):
        if self._parent:
            return self._parent.size
        else:
            return self._raw_surface_size
    
    @property
    def position(self):
        if self._fixed_position:
            x, y = self._fixed_position
        else:
            x, y = (self._relative_position[0] * self.surface_size[0], self._relative_position[1] * self.surface_size[1])

        if self._anchor_x == 'left':
            x = x
        elif self._anchor_x == 'right':
            x = self.surface_size[0] - x - self.size[0]
        elif self._anchor_x == 'center':
            x = (self.surface_size[0] / 2 - self.size[0] / 2) + x

        if self._anchor_y == 'top':
            y = y
        elif self._anchor_y == 'bottom':
            y = self.surface_size[1] - y - self.size[1]
        elif self._anchor_y == 'center':
            y = (self.surface_size[1] / 2 - self.size[1] / 2) + y

        if self._parent:
            return (x + self._parent.position[0], y + self._parent.position[1])
        else:
            return (x, y)
    
    @property
    def size(self):
        return (self._relative_size[0] * self.surface_size[1], self._relative_size[1] * self.surface_size[1])

    @property
    def margin(self):
        return self._relative_margin * self._raw_surface_size[1]

    @property
    def border_width(self):
        return self._relative_border_width * self._raw_surface_size[1]

    @property
    def border_radius(self):
        return self._relative_border_radius * self._raw_surface_size[1]

    @property
    def font_size(self):
        return self._relative_font_size * self.surface_size[1]
    
    def set_image(self):
        raise NotImplementedError
    
    def set_geometry(self):
        self.rect = self.image.get_rect()

        if self._anchor_x == 'left':
            if self._anchor_y == 'top':
                self.rect.topleft = self.position
            elif self._anchor_y == 'bottom':
                self.rect.topleft = self.position
            elif self._anchor_y == 'center':
                self.rect.topleft = self.position
        elif self._anchor_x == 'right':
            if self._anchor_y == 'top':
                self.rect.topleft = self.position
            elif self._anchor_y == 'bottom':
                self.rect.topleft = self.position
            elif self._anchor_y == 'center':
                self.rect.topleft = self.position
        elif self._anchor_x == 'center':
            if self._anchor_y == 'top':
                self.rect.topleft = self.position
            elif self._anchor_y == 'bottom':
                self.rect.topleft = self.position
            elif self._anchor_y == 'center':
                self.rect.topleft = self.position
    
    def set_surface_size(self, new_surface_size):
        self._raw_surface_size = new_surface_size
    
    def process_event(self, event):
        raise NotImplementedError

    def get_size(self):
        return self.size

    def blit(self, image, rect):
        self.image.blit(image, rect)

class _Pressable:
    def __init__(self, event, down_func=None, up_func=None, hover_func=None, prolonged=False, play_sfx=True, **kwargs):
        self._down_func = down_func
        self._up_func = up_func
        self._hover_func = hover_func
        self._pressed = False
        self._prolonged = prolonged
        self._play_sfx = play_sfx
        self._sfx = SFX['button_click']

        self._event = event

        self._widget_state = WidgetState.BASE

        self._colours = {}
    
    def set_state_colour(self, state):
        self._fill_colour = self._colours[state]

        self.set_image()
    
    def initialise_new_colours(self, colour):
        r, g, b, a = pygame.Color(colour).rgba

        self._colours = {
            WidgetState.BASE: pygame.Color(r, g, b, a),
            WidgetState.HOVER: pygame.Color(min(r + 25, 255), min(g + 25, 255), min(b + 25, 255), a),
            WidgetState.PRESS: pygame.Color(min(r + 50, 255), min(g + 50, 255), min(b + 50, 255), a)
        }
    
    def get_widget_state(self):
        return self._widget_state

    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self._down_func()
                    self._widget_state = WidgetState.PRESS
            
            case pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self._widget_state == WidgetState.PRESS:
                        if self._play_sfx:
                            audio.play_sfx(self._sfx)

                        self._up_func()
                        self._widget_state = WidgetState.HOVER
                        return self._event

                    elif self._widget_state == WidgetState.BASE:
                        self._hover_func()

                elif self._prolonged and self._widget_state == WidgetState.PRESS:
                    if self._play_sfx:
                        audio.play_sfx(self._sfx)
                    self._up_func()
                    self._widget_state = WidgetState.BASE
                    return self._event

            case pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self._widget_state == WidgetState.PRESS:
                        return
                    elif self._widget_state == WidgetState.BASE:
                        self._hover_func()
                        self._widget_state = WidgetState.HOVER
                    elif self._widget_state == WidgetState.HOVER:
                        self._hover_func()
                else:
                    if self._prolonged is False:
                        if self._widget_state in [WidgetState.PRESS, WidgetState.HOVER]:
                            self._widget_state = WidgetState.BASE
                            self._up_func()
                        elif self._widget_state == WidgetState.BASE:
                            return
                    elif self._prolonged is True:
                        if self._widget_state in [WidgetState.PRESS, WidgetState.BASE]:
                            return
                        else:
                            self._widget_state = WidgetState.BASE
                            self._up_func()

class _Circular:
    def __init__(self, items_dict, **kwargs):
        self._items_dict = items_dict
        self._keys_list = CircularLinkedList(list(items_dict.values()))
    
    @property
    def current_key(self):
        return self._keys_list.get_head().data

    @property
    def current_item(self):
        return self._items_dict[self.current_key]
    
    def set_next_item(self):
        self._keys_list.shift()

        self.set_image()
    
    def set_previous_item(self):
        self._keys_list.unshift()

        self.set_image()

    def set_to_key(self, key):
        if self._keys_list.data_in_list(key) is False:
            raise ValueError('(_Circular.set_to_key) Key not found:', key)
        
        for _ in range(len(self._widgets_dict)):
            if self.current_key == key:
                return

            self._keys_list.shift()