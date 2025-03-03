from data.constants import TranspositionFlag

class TranspositionEntry:
    def __init__(self, score, move, flag, hash_key, depth):
        self.score = score
        self.move = move
        self.flag = flag
        self.hash_key = hash_key
        self.depth = depth

class TranspositionTable:
    def __init__(self, max_entries=100000):
        self._max_entries = max_entries
        self._table = dict()
    
    def calculate_entry_index(self, hash_key):
        """
        Gets the dictionary key for a given Zobrist hash.

        Args:
            hash_key (int): A Zobrist hash.

        Returns:
            int: Key for the given hash.
        """
        # return hash_key % self._max_entries
        return hash_key
    
    def insert_entry(self, score, move, hash_key, depth, alpha, beta):
        """
        Inserts an entry into the transposition table.

        Args:
            score (int): The evaluation score.
            move (Move): The best move found.
            hash_key (int): The Zobrist hash key.
            depth (int): The depth of the search.
            alpha (int): The upper bound value.
            beta (int): The lower bound value.

        Raises:
            Exception: Invalid depth or score.
        """
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
            # Removes the longest-existing entry to free up space for more up-to-date entries
            # Expression to remove leftmost item taken from https://docs.python.org/3/library/collections.html#ordereddict-objects
            (k := next(iter(self._table)), self._table.pop(k))
    
    def get_entry(self, hash_key, depth, alpha, beta):
        """
        Gets an entry from the transposition table.

        Args:
            hash_key (int): The Zobrist hash key.
            depth (int): The depth of the search.
            alpha (int): The alpha value for pruning.
            beta (int): The beta value for pruning.

        Returns:
            tuple[int, Move] | tuple[None, None]: The evaluation score and the best move found, if entry exists.
        """
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