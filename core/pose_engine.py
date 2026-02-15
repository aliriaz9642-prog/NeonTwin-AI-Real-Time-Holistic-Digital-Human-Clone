import cv2
import time
import numpy as np
import mediapipe as mp

class PoseEngine:
    def __init__(self, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_holistic = mp.solutions.holistic
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_selfie = mp.solutions.selfie_segmentation
        
        self.holistic = self.mp_holistic.Holistic(
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            smooth_landmarks=True,
            refine_face_landmarks=True 
        )
        self.segmentor = self.mp_selfie.SelfieSegmentation(model_selection=1)
        self.prev_time = 0

    def process_frame(self, frame):
        """Processes a single frame and returns holistic results + segment mask."""
        start_time = time.perf_counter()
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_rgb.flags.writeable = False
        
        # Inference
        results = self.holistic.process(img_rgb)
        seg_results = self.segmentor.process(img_rgb)
        
        img_rgb.flags.writeable = True
        
        inference_time = (time.perf_counter() - start_time) * 1000 # ms
        
        return results, seg_results, inference_time

    def get_landmarks_array(self, results):
        """Converts pose landmarks to a NumPy array (33, 3)."""
        if not results.pose_landmarks:
            return None
        
        landmarks = []
        for lm in results.pose_landmarks.landmark:
            landmarks.append([lm.x, lm.y, lm.z])
        
        return np.array(landmarks)

    def draw_skeleton(self, frame, results, offset_x=0, color=(0, 255, 255), thickness=2, glow=True):
        """Draws a high-end NEON skeleton with glow and joint pulsing."""
        if not results.pose_landmarks:
            return frame

        h, w, _ = frame.shape
        t = time.time()
        
        # Pulse effect (sine wave)
        pulse = (np.sin(t * 5) + 1) / 2 # 0 to 1
        joint_radius = int(3 + pulse * 4)

        # 1. Draw Connection Lines (The 'Wireframe')
        for connection in self.mp_holistic.POSE_CONNECTIONS:
            start_idx, end_idx = connection
            lm_start = results.pose_landmarks.landmark[start_idx]
            lm_end = results.pose_landmarks.landmark[end_idx]
            
            p1 = (int(lm_start.x * w) + offset_x, int(lm_start.y * h))
            p2 = (int(lm_end.x * w) + offset_x, int(lm_end.y * h))
            
            if glow:
                # Layered drawing for Neon effect
                cv2.line(frame, p1, p2, color, thickness + 4) # Outer glow
                cv2.line(frame, p1, p2, (255, 255, 255), thickness - 1) # Inner core
            else:
                cv2.line(frame, p1, p2, color, thickness)

        # 2. Draw Joints with 'Heavy' Pulse
        for lm in results.pose_landmarks.landmark:
            center = (int(lm.x * w) + offset_x, int(lm.y * h))
            # Outer ring
            cv2.circle(frame, center, joint_radius + 2, color, 1)
            # Inner solid core
            cv2.circle(frame, center, 2, (255, 255, 255), -1)

        return frame

    def draw_hud(self, frame, results):
        """Draws the Main HUD with localized scanning effects."""
        # Draw User Skeleton with Cyber Green
        self.draw_skeleton(frame, results, offset_x=0, color=(0, 255, 150), thickness=2, glow=True)
        
        # Add 'Target Acquired' brackets if landmarks exist
        if results.pose_landmarks:
            h, w, _ = frame.shape
            cv2.rectangle(frame, (10, 10), (350, 180), (0, 255, 0), 1)
            cv2.putText(frame, "[ STATUS: TARGET LOCKED ]", (20, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        return frame

    def calculate_fps(self):
        curr_time = time.time()
        fps = 1 / (curr_time - self.prev_time) if self.prev_time != 0 else 0
        self.prev_time = curr_time
        return fps
