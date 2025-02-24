from data.constants import Rank, File, Piece, Colour, Rotation, RotationIndex, EMPTY_BB
from data.states.game.components.fen_parser import parse_fen_string
from data.states.game.cpu.zobrist_hasher import ZobristHasher
from data.utils import bitboard_helpers as bb_helpers
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)

class BitboardCollection:
    def __init__(self, fen_string):
        self.piece_bitboards = [{char: EMPTY_BB for char in Piece}, {char: EMPTY_BB for char in Piece}]
        self.combined_colour_bitboards = [EMPTY_BB, EMPTY_BB]
        self.combined_all_bitboard = EMPTY_BB
        self.rotation_bitboards = [EMPTY_BB, EMPTY_BB]
        self.active_colour = Colour.BLUE
        self._hasher = ZobristHasher()

        try:
            if fen_string:
                self.piece_bitboards, self.combined_colour_bitboards, self.combined_all_bitboard, self.rotation_bitboards, self.active_colour = parse_fen_string(fen_string)
                self.initialise_hash()
        except ValueError as error:
            logger.error('Please input a valid FEN string:', error)
            raise error
    
    def __str__(self):
        """
        Returns a string representation of the bitboards.

        Returns:
            str: Bitboards formatted with piece type and colour shown.
        """
        characters = ''
        for rank in reversed(Rank):
            for file in File:
                bitboard = 1 << (rank * 10 + file)

                colour = self.get_colour_on(bitboard)
                piece = self.get_piece_on(bitboard, Colour.BLUE) or self.get_piece_on(bitboard, Colour.RED)

                if piece is not None:
                        characters += f'{piece.upper() if colour == Colour.BLUE else piece}  '
                else:
                    characters += '.  '

            characters += '\n\n'
 
        return characters
    
    def get_rotation_string(self):
        """
        Returns a string representation of the board rotations.

        Returns:
            str: Board formatted with only rotations shown.
        """
        characters = ''
        for rank in reversed(Rank):

            for file in File:
                mask = 1 << (rank * 10 + file)
                rotation = self.get_rotation_on(mask)
                has_piece = bb_helpers.is_occupied(self.combined_all_bitboard, mask)

                if has_piece:
                    characters += f'{rotation.upper()}  '
                else:
                    characters += '.  '

            characters += '\n\n'
 
        return characters
    
    def initialise_hash(self):
        """
        Initialises the Zobrist hash for the current board state.
        """
        for piece in Piece:
            for colour in Colour:
                piece_bitboard = self.get_piece_bitboard(piece, colour)

                for occupied_bitboard in bb_helpers.occupied_squares(piece_bitboard):
                    self._hasher.apply_piece_hash(occupied_bitboard, piece, colour)
        
        for bitboard in bb_helpers.loop_all_squares():
            rotation = self.get_rotation_on(bitboard)
            self._hasher.apply_rotation_hash(bitboard, rotation)
                    
        if self.active_colour == Colour.RED:
            self._hasher.apply_red_move_hash()
    
    def flip_colour(self):
        """
        Flips the active colour and updates the Zobrist hash.
        """
        self.active_colour = self.active_colour.get_flipped_colour()

        if self.active_colour == Colour.RED:
            self._hasher.apply_red_move_hash()
    
    def update_move(self, src, dest):
        """
        Updates the bitboards for a move.

        Args:
            src (int): The bitboard representation of the source square.
            dest (int): The bitboard representation of the destination square.
        """
        piece = self.get_piece_on(src, self.active_colour)

        self.clear_square(src, Colour.BLUE)
        self.clear_square(dest, Colour.BLUE)
        self.clear_square(src, Colour.RED)
        self.clear_square(dest, Colour.RED)

        self.set_square(dest, piece, self.active_colour)
    
    def update_rotation(self, src, dest, new_rotation):
        """
        Updates the rotation bitboards for a move.

        Args:
            src (int): The bitboard representation of the source square.
            dest (int): The bitboard representation of the destination square.
            new_rotation (Rotation): The new rotation.
        """
        self.clear_rotation(src)
        self.set_rotation(dest, new_rotation)
    
    def clear_rotation(self, bitboard):
        """
        Clears the rotation for a given square.

        Args:
            bitboard (int): The bitboard representation of the square.
        """
        old_rotation = self.get_rotation_on(bitboard)
        rotation_1, rotation_2 = self.rotation_bitboards
        self.rotation_bitboards[RotationIndex.FIRSTBIT] = bb_helpers.clear_square(rotation_1, bitboard)
        self.rotation_bitboards[RotationIndex.SECONDBIT] = bb_helpers.clear_square(rotation_2, bitboard)

        self._hasher.apply_rotation_hash(bitboard, old_rotation)
    
    def clear_square(self, bitboard, colour):
        """
        Clears a square piece and rotation for a given colour.

        Args:
            bitboard (int): The bitboard representation of the square.
            colour (Colour): The colour to clear.
        """
        piece = self.get_piece_on(bitboard, colour)

        if piece is None:
            return
        
        piece_bitboard = self.get_piece_bitboard(piece, colour)
        colour_bitboard = self.combined_colour_bitboards[colour]
        all_bitboard = self.combined_all_bitboard

        self.piece_bitboards[colour][piece] = bb_helpers.clear_square(piece_bitboard, bitboard)
        self.combined_colour_bitboards[colour] = bb_helpers.clear_square(colour_bitboard, bitboard)
        self.combined_all_bitboard = bb_helpers.clear_square(all_bitboard, bitboard)

        self._hasher.apply_piece_hash(bitboard, piece, colour)
    
    def set_rotation(self, bitboard, rotation):
        """
        Sets the rotation for a given square.

        Args:
            bitboard (int): The bitboard representation of the square.
            rotation (Rotation): The rotation to set.
        """
        rotation_1, rotation_2 = self.rotation_bitboards
        self._hasher.apply_rotation_hash(bitboard, rotation)
        
        match rotation:
            case Rotation.UP:
                return
            case Rotation.RIGHT:
                self.rotation_bitboards[RotationIndex.FIRSTBIT] = bb_helpers.set_square(rotation_1, bitboard)
                return
            case Rotation.DOWN:
                self.rotation_bitboards[RotationIndex.SECONDBIT] = bb_helpers.set_square(rotation_2, bitboard)
                return
            case Rotation.LEFT:
                self.rotation_bitboards[RotationIndex.FIRSTBIT] = bb_helpers.set_square(rotation_1, bitboard)
                self.rotation_bitboards[RotationIndex.SECONDBIT] = bb_helpers.set_square(rotation_2, bitboard)
                return
            case _:
                raise ValueError('Invalid rotation input (bitboard.py):', rotation)
    
    def set_square(self, bitboard, piece, colour):
        """
        Sets a piece on a given square.

        Args:
            bitboard (int): The bitboard representation of the square.
            piece (Piece): The piece to set.
            colour (Colour): The colour of the piece.
        """
        piece_bitboard = self.get_piece_bitboard(piece, colour)
        colour_bitboard = self.combined_colour_bitboards[colour]
        all_bitboard = self.combined_all_bitboard

        self.piece_bitboards[colour][piece] = bb_helpers.set_square(piece_bitboard, bitboard)
        self.combined_colour_bitboards[colour] = bb_helpers.set_square(colour_bitboard, bitboard)
        self.combined_all_bitboard = bb_helpers.set_square(all_bitboard, bitboard)

        self._hasher.apply_piece_hash(bitboard, piece, colour)
    
    def get_piece_bitboard(self, piece, colour):
        """
        Gets the bitboard for a piece type for a given colour.

        Args:
            piece (Piece): The piece bitboard to get.
            colour (Colour): The colour of the piece.

        Returns:
            int: The bitboard representation for all squares occupied by that piece type.
        """
        return self.piece_bitboards[colour][piece]
    
    def get_piece_on(self, target_bitboard, colour):
        """
        Gets the piece on a given square for a given colour.

        Args:
            target_bitboard (int): The bitboard representation of the square.
            colour (Colour): The colour of the piece.

        Returns:
            Piece: The piece on the square, or None if square is empty.
        """
        if not (bb_helpers.is_occupied(self.combined_colour_bitboards[colour], target_bitboard)):
            return None
    
        return next(
            (piece for piece in Piece if 
                bb_helpers.is_occupied(self.get_piece_bitboard(piece, colour), target_bitboard)),
            None)

    def get_rotation_on(self, target_bitboard):
        """
        Gets the rotation on a given square.

        Args:
            target_bitboard (int): The bitboard representation of the square.

        Returns:
            Rotation: The rotation on the square.
        """
        rotationBits = [bb_helpers.is_occupied(self.rotation_bitboards[RotationIndex.SECONDBIT], target_bitboard), bb_helpers.is_occupied(self.rotation_bitboards[RotationIndex.FIRSTBIT], target_bitboard)]

        match rotationBits:
            case [False, False]:
                return Rotation.UP
            case [False, True]:
                return Rotation.RIGHT
            case [True, False]:
                return Rotation.DOWN
            case [True, True]:
                return Rotation.LEFT
    
    def get_colour_on(self, target_bitboard):
        """
        Gets the colour of the piece on a given square.

        Args:
            target_bitboard (int): The bitboard representation of the square.

        Returns:
            Colour: The colour of the piece on the square.
        """
        for piece in Piece:
            if self.get_piece_bitboard(piece, Colour.BLUE) & target_bitboard != EMPTY_BB:
                return Colour.BLUE
            elif self.get_piece_bitboard(piece, Colour.RED) & target_bitboard != EMPTY_BB:
                return Colour.RED

    def get_piece_count(self, piece, colour):
        """
        Gets the count of a given piece type and colour.

        Args:
            piece (Piece): The piece to count.
            colour (Colour): The colour of the piece.

        Returns:
            int: The number of that piece of that colour on the board.
        """
        return bb_helpers.pop_count(self.get_piece_bitboard(piece, colour))
    
    def get_hash(self):
        """
        Gets the Zobrist hash of the current board state.

        Returns:
            int: The Zobrist hash.
        """
        return self._hasher.hash
    
    def convert_to_piece_list(self):
        """
        Converts all bitboards to a list of pieces.

        Returns:
            list: Board represented as a 2D list of Piece and Rotation objects.
        """
        piece_list = []

        for i in range(80):
            if x := self.get_piece_on(1 << i, Colour.BLUE):
                rotation = self.get_rotation_on(1 << i)
                piece_list.append((x.upper(), rotation))
            elif y := self.get_piece_on(1 << i, Colour.RED):
                rotation = self.get_rotation_on(1 << i)
                piece_list.append((y, rotation))
            else:
                piece_list.append(None)

        return piece_list