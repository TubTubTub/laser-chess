import pygame
from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.setup.widget_dict import SETUP_WIDGETS
from data.constants import SetupEventType
from data.states.game.components.bitboard_collection import BitboardCollection
from data.states.game.components.piece_group import PieceGroup
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import draw_background
from data.utils.board_helpers import screen_pos_to_coords, coords_to_screen_pos
from data.components.audio import audio
from data.components.animation import animation
from data.theme import theme

class Setup(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()

        self._bitboards = None
        self._piece_group = None
        self._selected_coords = None
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning setup.py')

        return None
    
    def startup(self, persist):
        print('starting setup.py')
        self._widget_group = WidgetGroup(SETUP_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)

        self._bitboards = BitboardCollection(persist['FEN_STRING'])
        self._piece_group = PieceGroup()
        self._selected_coords = None

        # audio.play_music(MUSIC_PATHS['setup'])
        
        self.refresh_pieces()

        self.draw()
    
    def refresh_pieces(self):
        self._piece_group.initialise_pieces(self._bitboards.convert_to_piece_list(), SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)
    
    def get_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(resize_end=True)
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_coords = screen_pos_to_coords(event.pos, SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)

            if clicked_coords:
                self._selected_coords = clicked_coords
                return
        
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._selected_coords = None
            return

        match widget_event.type:
            case None:
                return

            case SetupEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
    
    def handle_resize(self, resize_end=False):
        self._widget_group.handle_resize(self._screen.get_size())
        self._piece_group.handle_resize(SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size, resize_end)
    
    def draw(self):
        draw_background(self._screen, GRAPHICS['temp_background'])
        self._widget_group.draw()
        self._piece_group.draw(self._screen)

        if self._selected_coords:
            square_size = SETUP_WIDGETS['chessboard'].size[0] / 10
            overlay_position = coords_to_screen_pos(self._selected_coords, SETUP_WIDGETS['chessboard'].position, square_size)
            pygame.draw.rect(self._screen, theme['borderPrimary'], (*overlay_position, square_size, square_size), width=int(theme['borderWidth']))
    
    def update(self, **kwargs):
        self.draw()