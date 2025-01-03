from data.constants import TranspositionFlag

class TranspositionEntry:
    def __init__(self, hash_key, depth, flag, score, best_move=None):
        self.hash_key = hash_key
        self.depth = depth
        self.flag = flag
        self.score = score
        self.best_move = best_move

class TranspositionTable:
    def __init__(self, max_entries=50000):
        self._max_entries = max_entries
        self._table = dict()
    
    def calculate_entry_index(self, zobrist_key):
        return zobrist_key % self._hash_size
    
    def insert_entry(self, hash_key, depth, flag, score, alpha, beta):
        if depth == 0 or alpha < score < beta:
            flag = TranspositionFlag.EXACT
        elif score <= alpha:
            flag = TranspositionFlag.UPPER
        elif score >= beta:
            flag = TranspositionFlag.LOWER
        else:
            raise Exception('(TranspositionTable.insert_entry)')
            
        entry = TranspositionEntry(hash_key, depth, flag, score)

        self._table[hash_key] = entry

        if len(self._table) > self._max_entries:
            # REMOVES FIRST ADDED ENTRY https://docs.python.org/3/library/collections.html#ordereddict-objects
            (k := next(iter(self._table)), self._table.pop(k))
    
    def get_entry(self, hash_key, depth, alpha, beta):
        if hash_key not in self._table:
            return None, None
        
        entry = self._table[hash_key]
        
        if entry.hash_key == hash_key:
            if entry.depth >= depth:
                if entry.flag == TranspositionFlag.LOWER:
                    return entry.move, entry.score
                
                if entry.flag == TranspositionFlag.EXACT and entry.score <= alpha:
                    return entry.move, alpha
                
                if entry.flag == TranspositionFlag.UPPER and entry.score >= beta:
                    return entry.move, beta

        return None, None