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
from data.utils.browser_helpers import get_winner_string
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

        self.initialise_widgets()
        self.simulate_all_moves()
        self.refresh_pieces()
        self.refresh_widgets()

        # audio.play_music(MUSIC_PATHS['menu'])
        print(self._moves)
        self.draw()
    
    def initialise_widgets(self):
        REVIEW_WIDGETS['move_list'].reset_move_list()
        REVIEW_WIDGETS['move_list'].kill()
        REVIEW_WIDGETS['scroll_area'].set_image()

        REVIEW_WIDGETS['winner_text'].update_text(f'WINNER: {get_winner_string(self._game_info['winner'])}')
        REVIEW_WIDGETS['blue_piece_display'].reset_piece_list()
        REVIEW_WIDGETS['red_piece_display'].reset_piece_list()
    
        if self._game_info['time_enabled']:
            REVIEW_WIDGETS['timer_disabled_text'].kill()
        else:
            REVIEW_WIDGETS['blue_timer'].kill()
            REVIEW_WIDGETS['red_timer'].kill()
    
    def refresh_widgets(self):
        REVIEW_WIDGETS['move_number_text'].update_text(f'MOVE NO: {(self._move_index + 1) / 2:.1f} / {len(self._moves) / 2:.1f}')
        REVIEW_WIDGETS['move_colour_text'].update_text(f'{self.calculate_colour(self._move_index + 1).name} TO MOVE')
        
        if self._game_info['time_enabled']:
            if self._move_index == -1:
                REVIEW_WIDGETS['blue_timer'].set_time(float(self._game_info['time']) * 60 * 1000)
                REVIEW_WIDGETS['red_timer'].set_time(float(self._game_info['time']) * 60 * 1000)
            else:
                REVIEW_WIDGETS['blue_timer'].set_time(float(self._moves[self._move_index]['blue_time']) * 60 * 1000)
                REVIEW_WIDGETS['red_timer'].set_time(float(self._moves[self._move_index]['red_time']) * 60 * 1000)
        
        REVIEW_WIDGETS['scroll_area'].set_image()
    
    def simulate_all_moves(self):
        for index, move_dict in enumerate(self._moves):
            laser_result = self._board.apply_move(move_dict['move'], fire_laser=True)
            self._moves[index]['laser_result'] = laser_result

            if laser_result.hit_square_bitboard:
                if laser_result.piece_colour == Colour.BLUE:
                    REVIEW_WIDGETS['red_piece_display'].add_piece(laser_result.piece_hit)
                elif laser_result.piece_colour == Colour.RED:
                    REVIEW_WIDGETS['blue_piece_display'].add_piece(laser_result.piece_hit)
                
            REVIEW_WIDGETS['move_list'].append_to_move_list(move_dict['unparsed_move'])
    
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
        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(resize_end=True)
            return

        widget_event = self._widget_group.process_event(event)

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

                self._board.undo_move(self._moves[self._move_index]['move'], laser_result=self._moves[self._move_index]['laser_result'])

                laser_result = self._moves[self._move_index]['laser_result']
                self._laser_draw.add_laser(laser_result, laser_colour=self.calculate_colour(self._move_index))

                if laser_result.hit_square_bitboard:
                    if laser_result.piece_colour == Colour.BLUE:
                        REVIEW_WIDGETS['red_piece_display'].remove_piece(laser_result.piece_hit)
                    elif laser_result.piece_colour == Colour.RED:
                        REVIEW_WIDGETS['blue_piece_display'].remove_piece(laser_result.piece_hit)
                
                REVIEW_WIDGETS['move_list'].pop_from_move_list()
                
                self._move_index = max(-1, self._move_index - 1)
                self._last_move = 'PREVIOUS'
                
                self.refresh_pieces()
                self.refresh_widgets()

            case ReviewEventType.NEXT_CLICK:
                if self._move_index + 1 >= len(self._moves) or len(self._moves) == 0:
                    return
                
                self._board.apply_move(self._moves[self._move_index + 1]['move'])

                laser_result = self._moves[self._move_index + 1]['laser_result']
                self._laser_draw.add_laser(laser_result, laser_colour=self.calculate_colour(self._move_index + 1))

                if laser_result.hit_square_bitboard:
                    if laser_result.piece_colour == Colour.BLUE:
                        REVIEW_WIDGETS['red_piece_display'].add_piece(laser_result.piece_hit)
                    elif laser_result.piece_colour == Colour.RED:
                        REVIEW_WIDGETS['blue_piece_display'].add_piece(laser_result.piece_hit)
                
                REVIEW_WIDGETS['move_list'].append_to_move_list(self._moves[self._move_index + 1]['unparsed_move'])

                self._move_index = min(len(self._moves) - 1, self._move_index + 1)
                self._last_move = 'NEXT'
                
                self.refresh_pieces()
                self.refresh_widgets()
    
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