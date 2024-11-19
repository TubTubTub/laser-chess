from data.constants import Colour
import pickle

class GameEntry:
    def __init__(self, game_states):
        self._game_states = game_states
    
    def convert_to_row(self, game_entry):
        return (self._game_states['CPU_ENABLED'], self._game_states['CPU_DEPTH'], self._game_states['WINNER'], self._game_states['TIME_ENABLED'], self._game_states['TIME'], len(self._game_states['MOVES']), self.convert_moves(self._game_states['MOVES']))
    
    def convert_moves(self, moves):
        return '|'.join([
            f'{move['time'][Colour.BLUE]};{move['time'][Colour.RED]};{move['move']};{pickle.dumps(move['laserResult'])}'
            for move in moves
        ])



# self.states = {
#     'CPU_ENABLED': game_config['CPU_ENABLED'],
#     'CPU_DEPTH': game_config['CPU_DEPTH'],
#     'AWAITING_CPU': False,
#     'WINNER': None,
#     'PAUSED': False,
#     'ACTIVE_COLOUR': Colour.BLUE,
#     'TIME_ENABLED': game_config['TIME_ENABLED'],
#     'TIME': game_config['TIME'],
#     'MOVES': []
# }


#     move_item = {
#     'time': {
#         Colour.BLUE: GAME_WIDGETS['blue_timer'].get_time(),
#         Colour.RED: GAME_WIDGETS['red_timer'].get_time()
#     },
#     'move': move_notation,
#     'laserResult': laser_result
# }