from core.pose_engine import PoseEngine
from core.smoother import LandmarkSmoother
from network.transmitter import PoseTransmitter
import numpy as np
import cv2
import time

def main():
    print("[INFO] Initializing SKELETAL CLONE Production System...")
    engine = PoseEngine(model_complexity=1)
    smoother = LandmarkSmoother()
    transmitter = PoseTransmitter()
    
    cap = cv2.VideoCapture(0)
    # 720p resolution for professional look
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("[INFO] SKELETAL CLONE Mode: ACTIVE")

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success: break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # 1. Process Holistic
            results, seg_results, inference_time = engine.process_frame(frame)
            raw_landmarks = engine.get_landmarks_array(results)
            
            # 2. Advanced Visualization Dashboard
            composite = frame.copy()
            
            # Draw User's Skeleton (Green Glow)
            composite = engine.draw_hud(composite, results)
            
            # Draw THE CLONE (Neon Magenta Ghost)
            clone_offset = int(w * 0.40)
            composite = engine.draw_skeleton(composite, results, offset_x=clone_offset, color=(255, 0, 200), thickness=3, glow=True)
            
            # 3. Data Transmission
            payload = {"pose": None, "left_hand": None, "right_hand": None, "metrics": {}}

            if raw_landmarks is not None:
                smoothed = smoother.apply(raw_landmarks)
                payload["pose"] = smoothed.tolist()
                
                # Calculate Movement Intensity (based on nose landmark velocity)
                nose = raw_landmarks[0]
                intensity = np.linalg.norm(nose[:2]) * 10 # Simple heuristic
                
                if results.left_hand_landmarks:
                    payload["left_hand"] = [[lm.x, lm.y, lm.z] for lm in results.left_hand_landmarks.landmark]
                if results.right_hand_landmarks:
                    payload["right_hand"] = [[lm.x, lm.y, lm.z] for lm in results.right_hand_landmarks.landmark]

                fps = engine.calculate_fps()
                payload["metrics"] = {"inference_ms": round(inference_time, 2), "fps": round(fps, 1), "intensity": round(intensity, 2)}
                transmitter.send_payload(payload)
                
                # Digital Dashboard Elements (Heavy UI)
                cv2.putText(composite, "AI ARCHITECT: NEON TWIN v2.5", (20, 45), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 255, 150), 1)
                cv2.line(composite, (20, 55), (340, 55), (0, 255, 150), 1)
                
                # Dynamic Performance Bars
                cv2.putText(composite, "INTENSITY", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.rectangle(composite, (100, 75), (340, 90), (50, 50, 50), -1)
                cv2.rectangle(composite, (100, 75), (100 + int(min( intensity * 50, 240)), 90), (0, 255, 255), -1)

                cv2.putText(composite, "LATENCY", (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.rectangle(composite, (100, 105), (340, 120), (50, 50, 50), -1)
                cv2.rectangle(composite, (100, 105), (100 + int(min(inference_time * 5, 240)), 120), (0, 150, 255), -1)

                cv2.putText(composite, f"FRAME RATE: {int(fps)} FPS", (20, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(composite, "STREAM: ENCRYPTED UDP", (180, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

            cv2.imshow("Production Neon Clone | AI Architect v2.5", composite)

            if cv2.waitKey(1) & 0xFF == ord('q'): break
                
    except KeyboardInterrupt:
        print("[INFO] Shutting down...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        transmitter.close()

if __name__ == "__main__":
    main()
