# AI-Based Real-Time Digital Human Clone

## 🚀 System Architecture
This project implements a high-performance **Perception-Rendering Pipeline**. The system is split into two main domains:

1.  **Computational Server (Python):** Handles Video capture, ML inference (MediaPipe), Vector Mathematics, and Temporal Smoothing.
2.  **Visualization Client (Unity/Unreal):** Handles 3D asset rendering, retargeting logic, and UI.

### Key Logic Flow
- **Capture:** `cv2.CAP_DSHOW` backend for sub-10ms frame acquisition.
- **Inference:** MediaPipe Pose Full Model for 3D landmark extraction.
- **Filtering:** One-Euro Filter for non-linear jitter suppression.
- **Inter-Process Communication:** UDP broadcasting of skeletal JSON packets.

---

## 🛠️ Performance Optimization Strategies
To maintain **30+ FPS** and **low latency**, the following optimizations have been implemented:
1.  **Asynchronous Networking:** The UDP transmitter does not wait for an acknowledgment, ensuring the perception loop never blocks.
2.  **Thread Concurrency:** In Unity, the UDP receiver runs on a background thread to prevent GUI/Rendering stalls.
3.  **Vectorization:** All joint calculations utilize `NumPy` C-extensions for hardware acceleration.
4.  **Inference Tuning:** `model_complexity=1` provides the best balance between precision and speed for real-time applications.

---

## 🔬 Research-Level Extensions
For a University thesis or publication, consider these extensions:
1.  **Gaze & Facial Expression Integration:** Add `MediaPipe Face Mesh` to synchronize eye gaze and lip movements.
2.  **Inverse Kinematics (IK) Solver:** Instead of direct landmark mapping, use Fabrik or CCD IK in Unity to calculate bone rotations from end-effectors only (Hands, Feet, Head).
3.  **Physics-Based Retargeting:** Implement gravity and collision detection so the clone interacts with the virtual environment.
4.  **LSTM-Based Prediction:** Use a Recurrent Neural Network to predict the next frame's pose, further reducing perceived latency.

---

## 📖 How to Run
1.  **Setup Python:**
    ```bash
    pip install -r requirements.txt
    python main.py
    ```
2.  **Setup Unity:**
    - Create a new Unity Project.
    - Add a Humanoid Avatar.
    - Attach `PoseReceiver.cs` to any GameObject.
    - Map the `bones` array to the Avatar's transforms.
