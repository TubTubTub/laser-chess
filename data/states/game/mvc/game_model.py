from data.states.game.components.move import Move
from data.states.game.components.board import Board
from data.states.game.components.fen_parser import encode_fen_string
from data.states.game.widget_dict import GAME_WIDGETS
from data.states.game.cpu.cpu_thread import CPUThread
from data.states.game.cpu.engines import ABMinimaxCPU

from data.utils.bitboard_helpers import is_occupied
from data.utils import input_helpers as ip_helpers
from data.components.custom_event import CustomEvent
from data.constants import Colour, GameEventType, EMPTY_BB

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
        
        self._cpu = ABMinimaxCPU(3, self.cpu_callback)
        self._cpu_thread = CPUThread(self._cpu)
        self._cpu_thread.start()

    def register_listener(self, listener, parent_class):
        self._listeners[parent_class].append(listener)
    
    def alert_listeners(self, event):
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
                    raise Exception('Unhandled alert type (GameModel.alert_listeners)')
    
    def set_winner(self, colour=None):
        self.states['WINNER'] = colour
    
    def toggle_paused(self):
        self.states['PAUSED'] = not self.states['PAUSED']
        game_event = CustomEvent.create_event(GameEventType.PAUSE_CLICK)
        self.alert_listeners(game_event)

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
    
    def make_move(self, move):
        #SWAPPED ACTIVE COLOUR TO BOTTOM SO MIGHT BE BUGGY
        # print(f'PLAYER MOVE: {self._board.get_active_colour().name}')
        colour = self._board.bitboards.get_colour_on(move.src)
        piece = self._board.bitboards.get_piece_on(move.src, colour)
        laser_result = self._board.apply_move(move, add_hash=True)

        self.alert_listeners(CustomEvent.create_event(GameEventType.SET_LASER, laser_result=laser_result))
        
        self.states['ACTIVE_COLOUR'] = self._board.get_active_colour()
        self.set_winner(self._board.check_win())

        move_notation = move.to_notation(colour, piece, laser_result.hit_square_bitboard)

        self.alert_listeners(CustomEvent.create_event(GameEventType.UPDATE_PIECES, move_notation=move_notation))

        move_item = {
            'time': {
                Colour.BLUE: GAME_WIDGETS['blue_timer'].get_time(),
                Colour.RED: GAME_WIDGETS['red_timer'].get_time()
            },
            'move': move_notation,
            'laserResult': laser_result
        }
        self.states['MOVES'].append(move_item)
    
    def make_cpu_move(self):
        self.states['AWAITING_CPU'] = True
        self._cpu_thread.start_cpu(self.get_board())
    
    def cpu_callback(self, move):
        print('MAKING MOVE', move)
        if self.states['WINNER'] is None:
            self.make_move(move)
            self.states['AWAITING_CPU'] = False
    
    def kill_thread(self):
        self._cpu_thread.kill_thread()
        self.states['AWAITING_CPU'] = False
    
    def is_selectable(self, bitboard):
        return is_occupied(self._board.bitboards.combined_colour_bitboards[self.states['ACTIVE_COLOUR']], bitboard)
    
    def get_available_moves(self, bitboard):
        if (bitboard & self._board.get_all_active_pieces()) != EMPTY_BB:
            return self._board.get_valid_squares(bitboard)
        
        return EMPTY_BB

    def get_piece_list(self):
        return self._board.get_piece_list()

    def get_piece_info(self, bitboard):
        colour = self._board.bitboards.get_colour_on(bitboard)
        rotation = self._board.bitboards.get_rotation_on(bitboard)
        piece = self._board.bitboards.get_piece_on(bitboard, colour)
        return (piece, colour, rotation)

    def get_fen_string(self):
        return encode_fen_string(self._board.bitboards)
    
    def get_board(self):
        return self._board