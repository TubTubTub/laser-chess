import pygame
from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.review.widget_dict import REVIEW_WIDGETS
from data.states.game.components.board import Board
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.laser_draw import LaserDraw
from data.constants import ReviewEventType, Colour
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import draw_background
from data.components.audio import audio
from data.components.game_entry import GameEntry

class Review(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._widget_group = None

        self._moves = []
        self._game_info = {}
        self._move_index = 0

        self._board = None
        self._piece_group = None
        self._laser_draw = None
    
    def cleanup(self):
        print('cleaning review.py')

        return None
    
    def startup(self, persist):
        print('starting review.py')
        self._widget_group = WidgetGroup(REVIEW_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)

        self._moves = GameEntry.parse_moves(persist.pop('moves', ''))
        self._game_info = persist
        self._move_index = len(self._moves) - 1 # REPRESENTS BOARD BEFORE MOVE AT INDEX PLAYED

        self._board = Board(self._game_info['start_fen_string'])
        self._piece_group = PieceGroup()
        self._laser_draw = LaserDraw(REVIEW_WIDGETS['chessboard'].position, REVIEW_WIDGETS['chessboard'].size)

        self.simulate_all_moves()
        self.refresh_pieces()

        # audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def simulate_all_moves(self):
        for index, move_dict in enumerate(self._moves):
            laser_result = self._board.apply_move(move_dict['move'], fire_laser=True)
            self._moves[index]['laser_result'] = laser_result
    
    def refresh_pieces(self):
        self._piece_group.initialise_pieces(self._board.get_piece_list(), REVIEW_WIDGETS['chessboard'].position, REVIEW_WIDGETS['chessboard'].size)
    
    def calculate_colour(self, move_number):
        if self._game_info['start_fen_string'][-1].lower() == 'b':
            initial_colour = Colour.BLUE
        elif self._game_info['start_fen_string'][-1].lower() == 'r':
            initial_colour = Colour.RED
        
        if move_number % 2 == 0:
            return initial_colour
        else:
            return initial_colour.get_flipped_colour()
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(resize_end=True)
            return

        if widget_event is None:
            return

        match widget_event.type:
            case None:
                return

            case ReviewEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
            
            case ReviewEventType.PREVIOUS_CLICK:
                if self._move_index < 0 or len(self._moves) == 0:
                    return

                self._board.undo_move(self._moves[self._move_index]['move'], laser_result=self._moves[self._move_index]['laser_result']) # TEMP laser_result=None
                self._laser_draw.add_laser(self._moves[self._move_index]['laser_result'], laser_colour=self.calculate_colour(self._move_index))
                self.refresh_pieces()

                self._just_undid = self._move_index
                self._move_index = max(-1, self._move_index - 1)

                self._last_move = 'PREVIOUS'

            case ReviewEventType.NEXT_CLICK:
                if self._move_index + 1 >= len(self._moves) or len(self._moves) == 0:
                    return
                
                self._board.apply_move(self._moves[self._move_index + 1]['move'])
                self._laser_draw.add_laser(self._moves[self._move_index + 1]['laser_result'], laser_colour=self.calculate_colour(self._move_index + 1))
                self.refresh_pieces()

                self._move_index = min(len(self._moves) - 1, self._move_index + 1)

                self._last_move = 'NEXT'
    
    def handle_resize(self, resize_end=False):
        self._widget_group.handle_resize(self._screen.get_size())
        self._piece_group.handle_resize(REVIEW_WIDGETS['chessboard'].position, REVIEW_WIDGETS['chessboard'].size, resize_end)
        self._laser_draw.handle_resize(REVIEW_WIDGETS['chessboard'].position, REVIEW_WIDGETS['chessboard'].size)
    
    def draw(self):
        draw_background(self._screen, GRAPHICS['temp_background'])
        self._widget_group.draw()
        self._piece_group.draw(self._screen)
        self._laser_draw.draw()
    
    def update(self, **kwargs):
        self.draw()