from data.components.move import Move
from data.components.laser import Laser

from data.constants import Colour, Piece, Rank, File, MoveType, EventType, RotationDirection, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK, EMPTY_BB
from data.components.game_event import GameEvent
from data.components import bitboard
from data.utils import bitboard_helpers as bb_helpers
from data.utils import input_helpers as ip_helpers

class Board:
    def __init__(self, fen_string="sc3ncfancpb2/2pc7/3Pd7/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b"):
        self.bitboards = bitboard.BitboardCollection(fen_string)
        self.status_text = self.bitboards.active_colour.name

        self._listeners = []
        self._selected_square = None
        self._pressed_on_board = False
        self._paused = False
    
    @property
    def clicked(self):
        return self._pressed_on_board and not self._paused
    
    def register_listener(self, listener):
        self._listeners.append(listener)
    
    def alert_listeners(self, event):
        for listener in self._listeners:
            match event.type:
                case EventType.UPDATE_PIECES:
                    listener(event)
                
                case EventType.REMOVE_PIECE:
                    listener(event)
                
                case EventType.SET_LASER:
                    listener(event)

                case _:
                    raise Exception('Unhandled alert type (Board.alert_listeners)')
    
    def get_piece_list(self):
        return self.bitboards.convert_to_piece_list()

    def __str__(self):
        characters = ''
        for rank in reversed(Rank):

            for file in File:
                mask = 1 << (rank * 10 + file)
                blue_piece = self.bitboards.get_piece_on(mask, Colour.BLUE)
                red_piece = self.bitboards.get_piece_on(mask, Colour.RED)

                if blue_piece:
                    characters += f'{blue_piece.upper()}  '
                elif red_piece:
                    characters += f'{red_piece}  '
                else:
                    characters += '0  '

            characters += '\n\n'
        
        characters += f'CURRENT PLAYER TO MOVE: {self.bitboards.active_colour.name}'
        return characters
    
    def flip_colour(self):
        if self.bitboards.active_colour == Colour.BLUE:
            self.bitboards.active_colour = Colour.RED
        elif self.bitboards.active_colour == Colour.RED:
            self.bitboards.active_colour = Colour.BLUE

    def get_move(self):
        while True:
            try:
                move_type = ip_helpers.parse_move_type(input('Input move type (m/r): '))
                src_square = ip_helpers.parse_notation(input("From: "))
                dest_square = ip_helpers.parse_notation(input("To: "))
                rotation = ip_helpers.parse_rotation(input("Enter rotation (a/b/c/d): "))
                return Move.instance_from_notation(move_type, src_square, dest_square, rotation)
            except ValueError as error:
                print('Input error (Board.get_move): ' + str(error))
    
    def check_win(self):
        if self.get_all_valid_squares(self.bitboards.active_colour) == EMPTY_BB:
            return self.bitboards.active_colour.get_flipped_colour()

        return None
    
    def apply_move(self, move):
        piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)

        if piece_symbol is None:
            raise ValueError('Invalid move - no piece found on source square')
        elif piece_symbol == Piece.SPHINX:
            raise ValueError('Invalid move - sphinx piece is immovable')

        if move.move_type == MoveType.MOVE:
            possible_moves = self.get_valid_squares(move.src)
            if bb_helpers.is_occupied(move.dest, possible_moves) is False:
                raise ValueError('Invalid move - destination square is occupied')

            piece_rotation = self.bitboards.get_rotation_on(move.src)

            self.bitboards.update_move(move.src, move.dest)
            self.bitboards.update_rotation(move.src, move.dest, piece_rotation)

        elif move.move_type == MoveType.ROTATE:

            piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)
            piece_rotation = self.bitboards.get_rotation_on(move.src)

            if move.rotation_direction == RotationDirection.CLOCKWISE:
                new_rotation = piece_rotation.get_clockwise()
            elif move.rotation_direction == RotationDirection.ANTICLOCKWISE:
                new_rotation = piece_rotation.get_anticlockwise()

            self.bitboards.update_rotation(move.src, move.src, new_rotation)

        self.alert_listeners(GameEvent.create_event(EventType.UPDATE_PIECES))
        print(f'PLAYER MOVE: {self.bitboards.active_colour.name}')
    
    def remove_piece(self, square_bitboard):
        self.bitboards.clear_square(square_bitboard, Colour.BLUE)
        self.bitboards.clear_square(square_bitboard, Colour.RED)
    
    def get_valid_squares(self, src_bitboard):
        target_top_left = (src_bitboard & A_FILE_MASK & EIGHT_RANK_MASK) << 9
        target_top_middle = (src_bitboard & EIGHT_RANK_MASK) << 10
        target_top_right = (src_bitboard & J_FILE_MASK & EIGHT_RANK_MASK) << 11
        target_middle_right = (src_bitboard & J_FILE_MASK) << 1

        target_bottom_right = (src_bitboard & J_FILE_MASK & ONE_RANK_MASK) >> 9
        target_bottom_middle = (src_bitboard & ONE_RANK_MASK) >> 10
        target_bottom_left = (src_bitboard & A_FILE_MASK & ONE_RANK_MASK)>> 11
        target_middle_left = (src_bitboard & A_FILE_MASK) >> 1

        possible_moves = target_top_left | target_top_middle | target_top_right | target_middle_right |	target_bottom_right | target_bottom_middle | target_bottom_left | target_middle_left

        valid_possible_moves = possible_moves & ~self.bitboards.combined_all_bitboard
        return valid_possible_moves
    
    def get_all_valid_squares(self, colour):
        all_valid_squares = EMPTY_BB
        for piece in Piece:
            piece_bitboard = self.bitboards.get_piece_bitboard(piece, colour)

            for square in bb_helpers.occupied_squares(piece_bitboard):
                valid_moves = self.get_valid_squares(square)
                all_valid_squares = all_valid_squares | valid_moves
            
        return all_valid_squares
    
    def get_all_active_pieces(self):
        active_pieces = self.bitboards.combined_colour_bitboards[self.bitboards.active_colour]
        sphinx_bitboard = self.bitboards.get_piece_bitboard(Piece.SPHINX, self.bitboards.active_colour)
        return active_pieces ^ sphinx_bitboard

    def fire_laser(self):
        laser = Laser(self.bitboards)

        if laser.hit_square_bitboard:
            self.remove_piece(laser.hit_square_bitboard)
            coords_to_remove = bb_helpers.bitboard_to_coords(laser.hit_square_bitboard)
            self.alert_listeners(GameEvent.create_event(EventType.REMOVE_PIECE, coords_to_remove=coords_to_remove))
        
        active_colour = self.bitboards.active_colour

        self.alert_listeners(GameEvent.create_event(EventType.SET_LASER, laser_path=laser.laser_path, active_colour=active_colour))