from data.states.game.components.move import Move
from data.states.game.components.laser import Laser

from data.constants import Colour, Piece, Rank, File, MoveType, RotationDirection, Miscellaneous, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK, EMPTY_BB
from data.states.game.components.bitboard_collection import BitboardCollection
from data.utils import bitboard_helpers as bb_helpers
from collections import defaultdict

class Board:
    def __init__(self, fen_string="sc3ncfcncpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b"):
        self.bitboards = BitboardCollection(fen_string)
        self.hash_list = [self.bitboards.get_hash()]

    def __str__(self):
        """
        Returns a string representation of the board.

        Returns:
            str: Board formatted as string.
        """
        characters = ''
        pieces = defaultdict(int)

        for rank in reversed(Rank):
            for file in File:
                mask = 1 << (rank * 10 + file)
                blue_piece = self.bitboards.get_piece_on(mask, Colour.BLUE)
                red_piece = self.bitboards.get_piece_on(mask, Colour.RED)

                if blue_piece:
                    pieces[blue_piece.value.upper()] += 1
                    characters += f'{blue_piece.upper()}  '
                elif red_piece:
                    pieces[red_piece.value] += 1
                    characters += f'{red_piece}  '
                else:
                    characters += '.  '

            characters += '\n\n'
        
        characters += str(dict(pieces))
        characters += f'\nCURRENT PLAYER TO MOVE: {self.bitboards.active_colour.name}\n'
        return characters
    
    def get_piece_list(self):
        """
        Converts the board bitboards to a list of pieces.

        Returns:
            list: List of Pieces.
        """
        return self.bitboards.convert_to_piece_list()

    def get_active_colour(self):
        """
        Gets the active colour.

        Returns:
            Colour: The active colour.
        """
        return self.bitboards.active_colour

    def to_hash(self):
        """
        Gets the hash of the current board state.

        Returns:
            int: A Zobrist hash.
        """
        return self.bitboards.get_hash()
    
    def check_win(self):
        """
        Checks for a Pharoah capture or threefold-repetition.

        Returns:
            Colour | Miscellaneous: The winning colour, or Miscellaneous.DRAW.
        """
        for colour in Colour:
            if self.bitboards.get_piece_bitboard(Piece.PHAROAH, colour) == EMPTY_BB:
                return colour.get_flipped_colour()

        if self.hash_list.count(self.hash_list[-1]) >= 3:
            return Miscellaneous.DRAW

        return None
    
    def apply_move(self, move, fire_laser=True, add_hash=False):
        """
        Applies a move to the board.

        Args:
            move (Move): The move to apply.
            fire_laser (bool): Whether to fire the laser after the move.
            add_hash (bool): Whether to add the board state hash to the hash list.

        Returns:
            Laser: The laser trajectory result.
        """
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

        laser = None
        if fire_laser:
            laser = self.fire_laser(add_hash)
        
        if add_hash:
            self.hash_list.append(self.bitboards.get_hash())

        self.bitboards.flip_colour()

        return laser
    
    def undo_move(self, move, laser_result):
        """
        Undoes a move on the board.

        Args:
            move (Move): The move to undo.
            laser_result (Laser): The laser trajectory result.
        """
        self.bitboards.flip_colour()
        
        if laser_result.hit_square_bitboard:
            # Get info of destroyed piece, and add it to the board again
            src = laser_result.hit_square_bitboard
            piece = laser_result.piece_hit
            colour = laser_result.piece_colour
            rotation = laser_result.piece_rotation

            self.bitboards.set_square(src, piece, colour)
            self.bitboards.clear_rotation(src)
            self.bitboards.set_rotation(src, rotation)
        
        # Create new Move object that is the inverse of the passed move
        if move.move_type == MoveType.MOVE:
            reversed_move = Move.instance_from_bitboards(MoveType.MOVE, move.dest, move.src)
        elif move.move_type == MoveType.ROTATE:
            reversed_move = Move.instance_from_bitboards(MoveType.ROTATE, move.src, move.src, move.rotation_direction.get_opposite())
        
        self.apply_move(reversed_move, fire_laser=False)
        self.bitboards.flip_colour()
    
    def remove_piece(self, square_bitboard):
        """
        Removes a piece from a given square.

        Args:
            square_bitboard (int): The bitboard representation of the square.
        """
        self.bitboards.clear_square(square_bitboard, Colour.BLUE)
        self.bitboards.clear_square(square_bitboard, Colour.RED)
        self.bitboards.clear_rotation(square_bitboard)
    
    def get_valid_squares(self, src_bitboard, colour=None):
        """
        Gets valid squares for a piece to move to.

        Args:
            src_bitboard (int): The bitboard representation of the source square.
            colour (Colour, optional): The active colour of the piece.

        Returns:
            int: The bitboard representation of valid squares.
        """
        target_top_left = (src_bitboard & A_FILE_MASK & EIGHT_RANK_MASK) << 9
        target_top_middle = (src_bitboard & EIGHT_RANK_MASK) << 10
        target_top_right = (src_bitboard & J_FILE_MASK & EIGHT_RANK_MASK) << 11
        target_middle_right = (src_bitboard & J_FILE_MASK) << 1

        target_bottom_right = (src_bitboard & J_FILE_MASK & ONE_RANK_MASK) >> 9
        target_bottom_middle = (src_bitboard & ONE_RANK_MASK) >> 10
        target_bottom_left = (src_bitboard & A_FILE_MASK & ONE_RANK_MASK)>> 11
        target_middle_left = (src_bitboard & A_FILE_MASK) >> 1

        possible_moves = target_top_left | target_top_middle | target_top_right | target_middle_right |	target_bottom_right | target_bottom_middle | target_bottom_left | target_middle_left
        
        if colour is not None:
            valid_possible_moves = possible_moves & ~self.bitboards.combined_colour_bitboards[colour]
        else:
            valid_possible_moves = possible_moves & ~self.bitboards.combined_all_bitboard

        return valid_possible_moves
    
    def get_all_valid_squares(self, colour):
        """
        Gets all valid squares for a given colour.

        Args:
            colour (Colour): The colour of the pieces.

        Returns:
            int: The bitboard representation of all valid squares.
        """
        piece_bitboard = self.bitboards.combined_colour_bitboards[colour]
        possible_moves = 0b0

        for square in bb_helpers.occupied_squares(piece_bitboard):
            possible_moves |= self.get_valid_squares(square)

        return possible_moves

    def get_all_active_pieces(self):
        """
        Gets all active pieces for the current player.

        Returns:
            int: The bitboard representation of all active pieces.
        """
        active_pieces = self.bitboards.combined_colour_bitboards[self.bitboards.active_colour]
        sphinx_bitboard = self.bitboards.get_piece_bitboard(Piece.SPHINX, self.bitboards.active_colour)
        return active_pieces ^ sphinx_bitboard

    def fire_laser(self, remove_hash):
        """
        Fires the laser and removes hit pieces.

        Args:
            remove_hash (bool): Whether to clear the hash list if a piece is hit.

        Returns:
            Laser: The result of firing the laser.
        """
        laser = Laser(self.bitboards)

        if laser.hit_square_bitboard:
            self.remove_piece(laser.hit_square_bitboard)

            if remove_hash:
                self.hash_list = [] # Remove all hashes for threefold repetition, as the position is impossible to be repeated after a piece is removed
        return laser
    
    def generate_square_moves(self, src):
        """
        Generates all valid moves for a piece on a given square.

        Args:
            src (int): The bitboard representation of the source square.

        Yields:
            Move: A valid move for the piece.
        """
        for dest in bb_helpers.occupied_squares(self.get_valid_squares(src)):
            yield Move(MoveType.MOVE, src, dest)
    
    def generate_all_moves(self, colour):
        """
        Generates all valid moves for a given colour.

        Args:
            colour (Colour): The colour of the pieces.

        Yields:
            Move: A valid move for the active colour.
        """
        sphinx_bitboard = self.bitboards.get_piece_bitboard(Piece.SPHINX, colour)
        # Remove source squares for Sphinx pieces, as they cannot be moved
        sphinx_masked_bitboard = self.bitboards.combined_colour_bitboards[colour] ^ sphinx_bitboard

        for square in bb_helpers.occupied_squares(sphinx_masked_bitboard):
            # Generate movement moves
            yield from self.generate_square_moves(square)

            # Generate rotational moves
            for rotation_direction in RotationDirection:
                yield Move(MoveType.ROTATE, square, rotation_direction=rotation_direction)