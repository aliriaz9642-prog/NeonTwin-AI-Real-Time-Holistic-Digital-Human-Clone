import numpy as np
import time

class OneEuroFilter:
    def __init__(self, min_cutoff=1.0, beta=0.0, d_cutoff=1.0, freq=30):
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        self.freq = float(freq)
        self.x_prev = None
        self.dx_prev = None
        self.last_time = None

    def _alpha(self, cutoff):
        tau = 1.0 / (2 * np.pi * cutoff)
        te = 1.0 / self.freq
        return 1.0 / (1.0 + tau / te)

    def filter(self, x, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        
        if self.last_time is None:
            self.last_time = timestamp
            self.x_prev = x
            self.dx_prev = np.zeros_like(x)
            return x

        te = timestamp - self.last_time
        if te <= 0: return self.x_prev
        
        self.freq = 1.0 / te
        self.last_time = timestamp

        # Update the derivative
        dx = (x - self.x_prev) / te
        edx = self.dx_prev + (self._alpha(self.d_cutoff) * (dx - self.dx_prev))
        self.dx_prev = edx

        # Update the value
        cutoff = self.min_cutoff + self.beta * np.abs(edx)
        out = self.x_prev + (self._alpha(cutoff) * (x - self.x_prev))
        self.x_prev = out
        
        return out

class LandmarkSmoother:
    def __init__(self, num_landmarks=33):
        # We filter each x, y, z coordinate
        self.filters = [OneEuroFilter(min_cutoff=0.5, beta=0.01) for _ in range(num_landmarks)]

    def apply(self, landmarks):
        """
        landmarks: np.array of shape (N, 3)
        """
        smoothed = np.zeros_like(landmarks)
        for i in range(len(landmarks)):
            smoothed[i] = self.filters[i].filter(landmarks[i])
        return smoothed
