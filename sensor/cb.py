class cb:
    def __init__(self, size):
        self.b = [0]*size
        self.i = 0
        self.sz = size
    def append(self, v):
        self.b[self.i] = v
        self.i = (self.i + 1) % self.sz

