from data.constants import Miscellaneous, Colour

def get_winner_string(winner):
    if winner is None:
        return 'UNFINISHED'
    elif winner == Miscellaneous.DRAW:
        return 'DRAW'
    else:
        return Colour(winner).name