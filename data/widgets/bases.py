import pygame
from data.constants import WidgetState
from data.components.audio import audio
from data.theme import theme
from data.assets import SFX, FONTS

DEFAULT_SURFACE = pygame.display.get_surface()
DEFAULT_FONT = FONTS['default']
REQUIRED_KWARGS = ['relative_position', 'relative_size']

class _Widget(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()

        for required_kwarg in REQUIRED_KWARGS:
            if required_kwarg not in kwargs:
                raise KeyError(f'(_Widget.__init__) Required keyword "{required_kwarg}" not in base kwargs')

        self._surface = None
        self._surface_size = None
        self._relative_position = None
        self._relative_size = None

        if kwargs.get('surface') is None:
            self._surface = DEFAULT_SURFACE
        else:
            self._surface = kwargs.get('surface')

        self._surface_size = self._surface.get_size()
        self._relative_position = kwargs.get('relative_position')
        self._relative_margin = theme['margin'] / self._surface_size[1]
        self._relative_border_width = theme['borderWidth'] / self._surface_size[1]
        self._relative_border_radius = theme['borderRadius'] / self._surface_size[1]
        self._border_colour = pygame.Color(theme['borderPrimary'])
        self._text_colour = pygame.Color(theme['textPrimary'])
        self._fill_colour = pygame.Color(theme['fillPrimary'])

        if kwargs.get('relative_size'):
            self._relative_size = ((kwargs.get('relative_size')[0] / self._surface_size[0]) * self._surface_size[1], kwargs.get('relative_size')[1])
        
        if 'margin' in kwargs:
            self._relative_margin = kwargs.get('margin') / self._surface_size[1]

            if (self._relative_margin * 2) >= min(self._relative_size[0], self._relative_size[1]):
                raise ValueError('(_Widget.__init__) Margin larger than specified size!')
        
        if 'border_width' in kwargs:
            self._relative_border_width = kwargs.get('border_width') / self._surface_size[1]
        
        if 'border_radius' in kwargs:
            self._relative_border_radius = kwargs.get('border_radius') / self._surface_size[1]
        
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
    def position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])
    
    @property
    def size(self):
        return (self._relative_size[0] * self._surface_size[1], self._relative_size[1] * self._surface_size[1])

    @property
    def margin(self):
        return self._relative_margin * self._surface_size[1]

    @property
    def border_width(self):
        return self._relative_border_width * self._surface_size[1]

    @property
    def border_radius(self):
        return self._relative_border_radius * self._surface_size[1]
    
    def set_image(self):
        raise NotImplementedError
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    
    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size
    
    def process_event(self, event):
        raise NotImplementedError

    def get_size(self):
        return self._size

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