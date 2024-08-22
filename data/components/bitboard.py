from data.components.constants import PIECE_SYMBOLS, Colour
from data.components.fenparser import parse_fen_string
from data.components import bitboard_helpers as bb_helpers

class BitboardCollection():
    def __init__(self, fen_string):
        self.piece_bitboards = None
        self.combined_colour_bitboards = None
        self.combined_all_bitboard = None
        self.rotation_bitboards = None
        self.active_colour = None

        try:
            self.piece_bitboards, self.combined_colour_bitboards, self.combined_all_bitboard, self.rotation_bitboards, self.active_colour = parse_fen_string(fen_string)
        except ValueError:
            print('Please input a valid FEN string')
    
    def update_bitboard_move(self, src, dest):
        piece = self.get_piece_on(src, self.active_colour)
        self.clear_square(src, Colour.BLUE)
        self.clear_square(dest, Colour.BLUE)
        self.clear_square(src, Colour.RED)
        self.clear_square(dest, Colour.RED)

        self.set_square(dest, piece, self.active_colour)
    
    def clear_square(self, index, colour):
        piece = self.get_piece_on(index, colour)

        if piece is None:
            return
        
        piece_bitboard = self.get_piece_bitboard(piece, colour)
        colour_bitboard = self.combined_colour_bitboards[colour]
        all_bitboard = self.combined_all_bitboard

        self.piece_bitboards[colour][piece] = bb_helpers.clear_square(piece_bitboard, index)
        self.combined_colour_bitboards[colour] = bb_helpers.clear_square(colour_bitboard, index)
        self.combined_all_bitbioard = bb_helpers.clear_square(all_bitboard, index)
    
    def set_square(self, index, piece, colour):
        piece_bitboard = self.get_piece_bitboard(piece, colour)
        colour_bitboard = self.combined_colour_bitboards[colour]
        all_bitboard = self.combined_all_bitboard

        self.piece_bitboards[colour][piece] = bb_helpers.set_square(piece_bitboard, index)
        self.combined_colour_bitboards[colour] = bb_helpers.set_square(colour_bitboard, index)
        self.combined_all_bitboard = bb_helpers.set_square(all_bitboard, index)
    
    def flip_colour(self):
        self.active_colour = int(self.active_colour == 0)
    
    def get_piece_bitboard(self, piece, colour):
        return self.piece_bitboards[colour][piece]
    
    def get_piece_on(self, index, colour):
        if not (bb_helpers.is_occupied(self.combined_colour_bitboards[colour], index)):
            return None
    
        return next(
            (piece for piece in PIECE_SYMBOLS if 
                bb_helpers.is_occupied(self.get_piece_bitboard(piece, colour), index)),
            None)