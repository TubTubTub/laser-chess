from data.states.game.components.move import Move
from data.utils.enums import Colour

class GameEntry:
    def __init__(self, game_states, final_fen_string):
        self._game_states = game_states
        self._final_fen_string = final_fen_string

    # Debug method used to print GameEntry row
    def __str__(self):
        return f'''
<GameEntry> :>
    CPU_ENABLED: {self._game_states['CPU_ENABLED']}
    CPU_DEPTH: {self._game_states['CPU_DEPTH']},
    WINNER: {self._game_states['WINNER']},
    TIME_ENABLED: {self._game_states['TIME_ENABLED']},
    TIME: {self._game_states['TIME']},
    NUMBER_OF_PLY: {len(self._game_states['MOVES'])},
    MOVES: {self.convert_moves(self._game_states['MOVES'])}
    FINAL FEN_STRING: {self._final_fen_string}
    START FEN STRING: {self._game_states['START_FEN_STRING']}
</GameEntry>
        '''

    def convert_to_row(self):
        return (self._game_states['CPU_ENABLED'], self._game_states['CPU_DEPTH'], self._game_states['WINNER'], self._game_states['TIME_ENABLED'], self._game_states['TIME'], len(self._game_states['MOVES']), self.convert_moves(self._game_states['MOVES']), self._game_states['START_FEN_STRING'], self._final_fen_string)

    # List comprehension used to format move dictionary into string
    def convert_moves(self, moves):
        return '|'.join([
            f'{round(move['time'][Colour.BLUE], 4)};{round(move['time'][Colour.RED], 4)};{move['move']}'
            for move in moves
        ])

    # Inverse method of convert_moves, converts string into dictionary of moves
    @staticmethod
    def parse_moves(move_str):
        moves = move_str.split('|')
        return [
            {
                'blue_time': move.split(';')[0],
                'red_time': move.split(';')[1],
                'move': Move.instance_from_notation(move.split(';')[2]),
                'unparsed_move': move.split(';')[2],
            } for move in moves if move != ''
        ]