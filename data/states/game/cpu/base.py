class BaseCPU:
    def __init__(self):
        raise NotImplementedError

    def find_move(self):
        raise NotImplementedError
    
    def search(self):
        raise NotImplementedError