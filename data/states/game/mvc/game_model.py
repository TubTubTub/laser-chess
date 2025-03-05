from data.states.game.components.fen_parser import encode_fen_string
from data.constants import Colour, GameEventType, EMPTY_BB
from data.states.game.widget_dict import GAME_WIDGETS
from data.states.game.cpu.cpu_thread import CPUThread
from data.components.custom_event import CustomEvent
from data.utils.bitboard_helpers import is_occupied
from data.states.game.components.board import Board
from data.utils import input_helpers as ip_helpers
from data.states.game.components.move import Move
from data.managers.logs import initialise_logger
from data.states.game.cpu.engines import *

logger = initialise_logger(__name__)

class GameModel:
    def __init__(self, game_config):
        self._listeners = {
            'game': [],
            'win': [],
            'pause': [],
        }
        self._board = Board(fen_string=game_config['FEN_STRING'])

        self.states = {
            'CPU_ENABLED': game_config['CPU_ENABLED'],
            'CPU_DEPTH': game_config['CPU_DEPTH'],
            'AWAITING_CPU': False,
            'WINNER': None,
            'PAUSED': False,
            'ACTIVE_COLOUR': game_config['COLOUR'],
            'TIME_ENABLED': game_config['TIME_ENABLED'],
            'TIME': game_config['TIME'],
            'START_FEN_STRING': game_config['FEN_STRING'],
            'MOVES': [],
            'ZOBRIST_KEYS': []
        }
        
        self._cpu = IDMinimaxCPU(self.states['CPU_DEPTH'], self.cpu_callback, verbose=False)
        self._cpu_thread = CPUThread(self._cpu)
        self._cpu_thread.start()
        self._cpu_move = None

        logger.info(f'Initialising CPU depth of {self.states['CPU_DEPTH']}')

    def register_listener(self, listener, parent_class):
        """
        Registers listener method of another MVC class.

        Args:
            listener (callable): Listener callback function.
            parent_class (str): Class name.
        """
        self._listeners[parent_class].append(listener)
    
    def alert_listeners(self, event):
        """
        Alerts all registered classes of an event by calling their listener function.

        Args:
            event (GameEventType): Event to pass as argument.

        Raises:
            Exception: If an unrecgonised event tries to be passed onto listeners.
        """
        for parent_class, listeners in self._listeners.items():
            match event.type:
                case GameEventType.UPDATE_PIECES:
                    if parent_class in 'game':
                        for listener in listeners: listener(event)
                
                case GameEventType.SET_LASER:
                    if parent_class == 'game':
                        for listener in listeners: listener(event)
                
                case GameEventType.PAUSE_CLICK:
                    if parent_class in ['pause', 'game']:
                        for listener in listeners:
                            listener(event)

                case _:
                    raise Exception('Unhandled event type (GameModel.alert_listeners)')
    
    def set_winner(self, colour=None):
        """
        Sets winner.

        Args:
            colour (Colour, optional): Describes winnner colour, or draw. Defaults to None.
        """
        self.states['WINNER'] = colour
    
    def toggle_paused(self):
        """
        Toggles pause screen, and alerts pause view.
        """
        self.states['PAUSED'] = not self.states['PAUSED']
        game_event = CustomEvent.create_event(GameEventType.PAUSE_CLICK)
        self.alert_listeners(game_event)

    def get_terminal_move(self):
        """
        Debugging method for inputting a move from the terminal.

        Returns:
            Move: Parsed move.
        """
        while True:
            try:
                move_type = ip_helpers.parse_move_type(input('Input move type (m/r): '))
                src_square = ip_helpers.parse_notation(input("From: "))
                dest_square = ip_helpers.parse_notation(input("To: "))
                rotation = ip_helpers.parse_rotation(input("Enter rotation (a/b/c/d): "))
                return Move.instance_from_notation(move_type, src_square, dest_square, rotation)
            except ValueError as error:
                logger.warning('Input error (Board.get_move): ' + str(error))
    
    def make_move(self, move):
        """
        Takes a Move object and applies it to the board.

        Args:
            move (Move): Move to apply.
        """
        colour = self._board.bitboards.get_colour_on(move.src)
        piece = self._board.bitboards.get_piece_on(move.src, colour)
        # Apply move and get results of laser trajectory
        laser_result = self._board.apply_move(move, add_hash=True)

        self.alert_listeners(CustomEvent.create_event(GameEventType.SET_LASER, laser_result=laser_result))
        
        # Sets new active colour and checks for a win
        self.states['ACTIVE_COLOUR'] = self._board.get_active_colour()
        self.set_winner(self._board.check_win())

        move_notation = move.to_notation(colour, piece, laser_result.hit_square_bitboard)

        self.alert_listeners(CustomEvent.create_event(GameEventType.UPDATE_PIECES, move_notation=move_notation))
        
        # Adds move to move history list for review screen
        self.states['MOVES'].append({
            'time': {
                Colour.BLUE: GAME_WIDGETS['blue_timer'].get_time(),
                Colour.RED: GAME_WIDGETS['red_timer'].get_time()
            },
            'move': move_notation,
            'laserResult': laser_result
        })
    
    def make_cpu_move(self):
        """
        Starts CPU calculations on the separate thread.
        """
        self.states['AWAITING_CPU'] = True
        self._cpu_thread.start_cpu(self.get_board())
    
    def cpu_callback(self, move):
        """
        Callback function passed to CPU thread. Called when CPU stops processing.

        Args:
            move (Move): Move that CPU found.
        """
        if self.states['WINNER'] is None:
            # CPU move passed back to main threadby reassigning variable
            self._cpu_move = move
            self.states['AWAITING_CPU'] = False
    
    def check_cpu(self):
        """
        Constantly checks if CPU calculations are finished, so that make_move can be run on the main thread.
        """
        if self._cpu_move is not None:
            self.make_move(self._cpu_move)
            self._cpu_move = None
    
    def kill_thread(self):
        """
        Interrupt and kill CPU thread.
        """
        self._cpu_thread.kill_thread()
        self.states['AWAITING_CPU'] = False
    
    def is_selectable(self, bitboard):
        """
        Checks if square is occupied by a piece of the current active colour.

        Args:
            bitboard (int): Bitboard representing single square.

        Returns:
            bool: True if square is occupied by a piece of the current active colour. False if not.
        """
        return is_occupied(self._board.bitboards.combined_colour_bitboards[self.states['ACTIVE_COLOUR']], bitboard)
    
    def get_available_moves(self, bitboard):
        """
        Gets all surrounding empty squares. Used for drawing overlay.

        Args:
            bitboard (int): Bitboard representing single center square.

        Returns:
            int: Bitboard representing all empty surrounding squares.
        """
        if (bitboard & self._board.get_all_active_pieces()) != EMPTY_BB:
            return self._board.get_valid_squares(bitboard)
        
        return EMPTY_BB

    def get_piece_list(self):
        """
        Returns:
            list[Piece, ...]: Array of all pieces on the board.
        """
        return self._board.get_piece_list()

    def get_piece_info(self, bitboard):
        """
        Args:
            bitboard (int): Square containing piece.

        Returns:
            tuple[Colour, Rotation, Piece]: Piece information.
        """
        colour = self._board.bitboards.get_colour_on(bitboard)
        rotation = self._board.bitboards.get_rotation_on(bitboard)
        piece = self._board.bitboards.get_piece_on(bitboard, colour)
        return (piece, colour, rotation)

    def get_fen_string(self):
        return encode_fen_string(self._board.bitboards)
    
    def get_board(self):
        return self._board