from collections import deque
class CircularBuffer(object):
    buffer_methods = ('list', 'deque', 'roll')

    def __init__(self, buffer_size, buffer_method):
        self.content = None
        self.size = buffer_size
        self.method = buffer_method

    def append(self, scalar):
        if self.method == self.buffer_methods[0]:
            # Use list
            try:
                self.content.append(scalar)
                self.content.pop(0)
            except AttributeError:
                self.content = [0.] * self.size
        elif self.method == self.buffer_methods[1]:
            # Use collections.deque
            try:
                self.content.append(scalar)
            except AttributeError:
                self.content = collections.deque([0.] * self.size,
                                                 maxlen=self.size)
        elif self.method == self.buffer_methods[2]:
            # Use Numpy.roll
            try:
                self.content = numpy.roll(self.content, -1)
                self.content[-1] = scalar
            except IndexError:
                self.content = numpy.zeros(self.size, dtype=float)

