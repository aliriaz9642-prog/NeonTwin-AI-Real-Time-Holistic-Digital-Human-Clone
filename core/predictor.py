import numpy as np

class PosePredictor:
    def __init__(self, window_size=5, prediction_steps=2):
        self.window_size = window_size
        self.prediction_steps = prediction_steps
        self.history = []

    def predict(self, current_landmarks):
        """
        Uses velocity-based linear extrapolation to predict future pose.
        landmarks shape: (33, 3)
        """
        self.history.append(current_landmarks)
        if len(self.history) > self.window_size:
            self.history.pop(0)

        if len(self.history) < 2:
            return current_landmarks

        # Calculate average velocity over the window
        velocities = []
        for i in range(1, len(self.history)):
            velocities.append(self.history[i] - self.history[i-1])
        
        avg_velocity = np.mean(velocities, axis=0)
        
        # Predict future position
        # Next position = current + velocity * prediction_steps
        predicted_pose = current_landmarks + (avg_velocity * self.prediction_steps)
        
        return predicted_pose
