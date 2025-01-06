import threading
import time

class CPUThread(threading.Thread):
    def __init__(self, cpu):
        super().__init__()
        self._stop_event = threading.Event()
        self._running = True
        self.daemon = True

        self._board = None
        self._cpu = cpu
    
    def kill_thread(self):
        self.stop_cpu()
        self._running = False
    
    def stop_cpu(self):
        self._stop_event.set()
        self._board = None
    
    def start_cpu(self, board):
        self._stop_event.clear()
        self._board = board
    
    def run(self):
        while self._running:
            if self._board and self._cpu:
                self._cpu.find_move(self._board, self._stop_event)
                self.stop_cpu()
            else:
                time.sleep(1)
                print(f'(CPUThread.run) Thread {threading.get_native_id()} idling...')