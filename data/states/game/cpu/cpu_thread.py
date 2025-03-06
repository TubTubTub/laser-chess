import threading
import time
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)

class CPUThread(threading.Thread):
    def __init__(self, cpu, verbose=False):
        super().__init__()
        self._stop_event = threading.Event()
        self._running = True
        self._verbose = verbose
        self.daemon = True

        self._board = None
        self._cpu = cpu
        self._id = None
    
    def kill_thread(self):
        """
        Kills the CPU and terminates the thread by stopping the run loop.
        """
        self.stop_cpu(force=True)
        self._running = False
    
    def stop_cpu(self, id=None, force=False):
        """
        Kills the CPU's move search.

        Args:
            id (int, optional): Id of search to kill, only kills if matching.
            force (bool, optional): Forcibly kill search regardless of id.
        """
        if self._id == id or force:
            self._stop_event.set()
            self._board = None
    
    def start_cpu(self, board, id=None):
        """
        Starts the CPU's move search.

        Args:
            board (Board): The current board state.
            id (int, optional): Id of current search.
        """
        self._stop_event.clear()
        self._board = board
        self._id = id
    
    def run(self):
        """
        Periodically checks if the board variable is set.
        If it is, then starts CPU search.
        """
        while self._running:
            if self._board and self._cpu:
                self._cpu.find_move(self._board, self._stop_event)
                self.stop_cpu()
            else:
                time.sleep(1)
                if self._verbose:
                    logger.debug(f'(CPUThread.run) Thread {threading.get_native_id()} idling...')