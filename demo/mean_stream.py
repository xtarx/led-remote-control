class MeanStream:
    def __init__(self, size):
        self.size = float(size)
        self.accumulated = 0.
        self.numbers = [0]*size
        self._mean = 0.

    def add(self, num):
        i = int(self.accumulated) % int(self.size)
        self.accumulated += 1
        if self.accumulated <= self.size:
            self._mean = self._mean*(self.accumulated-1) + num
            self._mean /= self.accumulated
            self.numbers[i] = num
        else:
            self._mean = self._mean*self.size - self.numbers[i] + num
            self._mean /= self.size
            self.numbers[i] = num


    @property
    def mean(self):
        return self._mean

