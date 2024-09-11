from data.constants import MoveType, Rotation

def parse_move_type(move_type):
    if type(move_type) != 'string':
        raise ValueError('Invalid move type - move type must be a string!')
    if move_type.lower() not in MoveType:
        raise ValueError('Invalid move - type - move type must be m or r!')
    
    return MoveType[move_type.lower()]

def parse_notation(notation):
    if type(notation) != 'string':
        raise ValueError('Invalid notation - notation must be a string!')
    if not (97 <= ord(notation[0]) <= 106):
        raise ValueError('Invalid notation - file is out of range!')
    elif not (0 <= int(notation[1]) <= 10):
        raise ValueError('Invalid notation - rank is out of range!')
    
    return notation

def parse_rotation(rotation):
    if type(rotation) != 'string':
        raise ValueError('Invalid rotation - rotation must be a string!')
    if rotation.lower() not in Rotation:
        raise ValueError('Invalid rotation - rotation is invalid!')
    
    return Rotation[rotation.lower()]