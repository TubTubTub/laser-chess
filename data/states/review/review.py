import pygame
from data.states.game.components.capture_draw import CaptureDraw
from data.states.game.components.piece_group import PieceGroup
from data.constants import ReviewEventType, Colour, ShaderType
from data.states.game.components.laser_draw import LaserDraw
from data.states.review.widget_dict import REVIEW_WIDGETS
from data.utils.bitboard_helpers import bitboard_to_coords
from data.utils.browser_helpers import get_winner_string
from data.states.game.components.board import Board
from data.components.game_entry import GameEntry
from data.managers.logs import initialise_logger
from data.managers.window import window
from data.assets import MUSIC
from data.control import _State

logger = initialise_logger(__name__)

class Review(_State):
    def __init__(self):
        super().__init__()

        self._moves = []
        self._game_info = {}
        self._move_index = 0

        self._board = None
        self._piece_group = None
        self._laser_draw = None
        self._capture_draw = None
    
    def cleanup(self):
        super().cleanup()
        
        window.clear_apply_arguments(ShaderType.BLOOM)

        return None
    
    def startup(self, persist):
        super().startup(REVIEW_WIDGETS, MUSIC['menu'])

        window.set_apply_arguments(ShaderType.BASE, background_type=ShaderType._BACKGROUND_BALATRO)
        window.set_apply_arguments(ShaderType.BLOOM, occlusion_colours=[(pygame.Color('0x95e0cc')).rgb, pygame.Color('0xf14e52').rgb], colour_intensity=0.8)
        REVIEW_WIDGETS['help'].kill()

        self._moves = GameEntry.parse_moves(persist.pop('moves', ''))
        self._game_info = persist
        self._move_index = len(self._moves) - 1 # REPRESENTS BOARD BEFORE MOVE AT INDEX PLAYED

        self._board = Board(self._game_info['start_fen_string'])
        self._piece_group = PieceGroup()
        self._laser_draw = LaserDraw(self.board_position, self.board_size)
        self._capture_draw = CaptureDraw(self.board_position, self.board_size)

        self.initialise_widgets()
        self.simulate_all_moves()
        self.refresh_pieces()
        self.refresh_widgets()

        self.draw()
        
        print(self._moves)
    
    @property
    def board_position(self):
        return REVIEW_WIDGETS['chessboard'].position
    
    @property
    def board_size(self):
        return REVIEW_WIDGETS['chessboard'].size

    @property
    def square_size(self):
        return self.board_size[0] / 10
    
    def initialise_widgets(self):
        REVIEW_WIDGETS['move_list'].reset_move_list()
        REVIEW_WIDGETS['move_list'].kill()
        REVIEW_WIDGETS['scroll_area'].set_image()

        REVIEW_WIDGETS['winner_text'].set_text(f'WINNER: {get_winner_string(self._game_info['winner'])}')
        REVIEW_WIDGETS['blue_piece_display'].reset_piece_list()
        REVIEW_WIDGETS['red_piece_display'].reset_piece_list()
    
        if self._game_info['time_enabled']:
            REVIEW_WIDGETS['timer_disabled_text'].kill()
        else:
            REVIEW_WIDGETS['blue_timer'].kill()
            REVIEW_WIDGETS['red_timer'].kill()
    
    def refresh_widgets(self):
        REVIEW_WIDGETS['move_number_text'].set_text(f'MOVE NO: {(self._move_index + 1) / 2:.1f} / {len(self._moves) / 2:.1f}')
        REVIEW_WIDGETS['move_colour_text'].set_text(f'{self.calculate_colour(self._move_index + 1).name} TO MOVE')
        
        if self._game_info['time_enabled']:
            if self._move_index == -1:
                REVIEW_WIDGETS['blue_timer'].set_time(float(self._game_info['time']) * 60 * 1000)
                REVIEW_WIDGETS['red_timer'].set_time(float(self._game_info['time']) * 60 * 1000)
            else:
                REVIEW_WIDGETS['blue_timer'].set_time(float(self._moves[self._move_index]['blue_time']) * 60 * 1000)
                REVIEW_WIDGETS['red_timer'].set_time(float(self._moves[self._move_index]['red_time']) * 60 * 1000)
        
        REVIEW_WIDGETS['scroll_area'].set_image()
    
    def refresh_pieces(self):
        self._piece_group.initialise_pieces(self._board.get_piece_list(), self.board_position, self.board_size)
    
    def simulate_all_moves(self):
        for index, move_dict in enumerate(self._moves):
            laser_result = self._board.apply_move(move_dict['move'], fire_laser=True)
            self._moves[index]['laser_result'] = laser_result

            if laser_result.hit_square_bitboard:
                if laser_result.piece_colour == Colour.BLUE:
                    REVIEW_WIDGETS['red_piece_display'].add_piece(laser_result.piece_hit)
                elif laser_result.piece_colour == Colour.RED:
                    REVIEW_WIDGETS['blue_piece_display'].add_piece(laser_result.piece_hit)
                print('adding piece')
                
            REVIEW_WIDGETS['move_list'].append_to_move_list(move_dict['unparsed_move'])
    
    def calculate_colour(self, move_number):
        if self._game_info['start_fen_string'][-1].lower() == 'b':
            initial_colour = Colour.BLUE
        elif self._game_info['start_fen_string'][-1].lower() == 'r':
            initial_colour = Colour.RED
        
        if move_number % 2 == 0:
            return initial_colour
        else:
            return initial_colour.get_flipped_colour()
    
    def handle_move(self, move_index, add_piece=True):
        laser_result = self._moves[move_index]['laser_result']
        self._laser_draw.add_laser(laser_result, laser_colour=self.calculate_colour(move_index))

        if laser_result.hit_square_bitboard:
            if laser_result.piece_colour == Colour.BLUE:
                if add_piece:
                    REVIEW_WIDGETS['red_piece_display'].add_piece(laser_result.piece_hit)
                else:
                    REVIEW_WIDGETS['red_piece_display'].remove_piece(laser_result.piece_hit)
            elif laser_result.piece_colour == Colour.RED:
                if add_piece:
                    REVIEW_WIDGETS['blue_piece_display'].add_piece(laser_result.piece_hit)
                else:
                    REVIEW_WIDGETS['blue_piece_display'].remove_piece(laser_result.piece_hit)

            self._capture_draw.add_capture(
                laser_result.piece_hit,
                laser_result.piece_colour,
                laser_result.piece_rotation,
                bitboard_to_coords(laser_result.hit_square_bitboard),
                laser_result.laser_path[0][0],
                self.calculate_colour(move_index),
                shake=False
            )
    
    def update_laser_mask(self):
        temp_surface = pygame.Surface(window.size, pygame.SRCALPHA)
        self._piece_group.draw(temp_surface)
        mask = pygame.mask.from_surface(temp_surface, threshold=127)
        mask_surface = mask.to_surface(unsetcolor=(0, 0, 0, 255), setcolor=(255, 0, 0, 255))

        window.set_apply_arguments(ShaderType.RAYS, occlusion=mask_surface)

    def get_event(self, event):
        if event.type in [pygame.MOUSEBUTTONUP, pygame.KEYDOWN]:
            REVIEW_WIDGETS['help'].kill()

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
                
                self._move_index = max(-1, self._move_index - 1)

                self._board.undo_move(self._moves[self._move_index + 1]['move'], laser_result=self._moves[self._move_index + 1]['laser_result'])
                self.handle_move(self._move_index + 1, add_piece=False)
                REVIEW_WIDGETS['move_list'].pop_from_move_list()
                
                self.refresh_pieces()
                self.refresh_widgets()
                self.update_laser_mask()

            case ReviewEventType.NEXT_CLICK:
                if self._move_index + 1 >= len(self._moves) or len(self._moves) == 0:
                    return
                
                self._move_index = min(len(self._moves) - 1, self._move_index + 1)
                
                self._board.apply_move(self._moves[self._move_index]['move'])
                self.handle_move(self._move_index, add_piece=True)
                REVIEW_WIDGETS['move_list'].append_to_move_list(self._moves[self._move_index]['unparsed_move'])
                
                self.refresh_pieces()
                self.refresh_widgets()
                self.update_laser_mask()
            
            case ReviewEventType.HELP_CLICK:
                self._widget_group.add(REVIEW_WIDGETS['help'])
                self._widget_group.handle_resize(window.size)
    
    def handle_resize(self):
        super().handle_resize()
        self._piece_group.handle_resize(self.board_position, self.board_size)
        self._laser_draw.handle_resize(self.board_position, self.board_size)
        self._capture_draw.handle_resize(self.board_position, self.board_size)

        if self._laser_draw.firing:
            self.update_laser_mask()

    def draw(self):
        self._capture_draw.update()
        self._widget_group.draw()
        self._piece_group.draw(window.screen)
        self._laser_draw.draw(window.screen)
        self._capture_draw.draw(window.screen)