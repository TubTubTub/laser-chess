from data.constants import TranspositionFlag

class TranspositionEntry:
    def __init__(self, score, move, flag, hash_key, depth):
        self.score = score
        self.move = move
        self.flag = flag
        self.hash_key = hash_key
        self.depth = depth

class TranspositionTable:
    def __init__(self, max_entries=50000):
        self._max_entries = max_entries
        self._table = dict()
    
    def calculate_entry_index(self, hash_key):
        # return hash_key % self._max_entries
        return str(hash_key)
    
    def insert_entry(self, score, move, hash_key, depth, alpha, beta):
        if depth == 0 or alpha < score < beta:
            flag = TranspositionFlag.EXACT
            score = score
        elif score <= alpha:
            flag = TranspositionFlag.UPPER
            score = alpha
        elif score >= beta:
            flag = TranspositionFlag.LOWER
            score = beta
        else:
            raise Exception('(TranspositionTable.insert_entry)')

        self._table[self.calculate_entry_index(hash_key)] = TranspositionEntry(score, move, flag, hash_key, depth)

        if len(self._table) > self._max_entries:
            # REMOVES FIRST ADDED ENTRY https://docs.python.org/3/library/collections.html#ordereddict-objects
            (k := next(iter(self._table)), self._table.pop(k))
    
    def get_entry(self, hash_key, depth, alpha, beta):
        index = self.calculate_entry_index(hash_key)
        
        if index not in self._table:
            return None, None
        
        entry = self._table[index]
        
        if entry.hash_key == hash_key and entry.depth >= depth:
            if entry.flag == TranspositionFlag.EXACT:
                return entry.score, entry.move
            
            if entry.flag == TranspositionFlag.LOWER and entry.score >= beta:
                return entry.score, entry.move
            
            if entry.flag == TranspositionFlag.UPPER and entry.score <= alpha:
                return entry.score, entry.move

        return None, None