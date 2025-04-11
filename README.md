# AspirexCVWS
# 🎨 Virtual Painter using Hand Detection

This project is a Virtual Painter that uses hand tracking powered by [MediaPipe]([https://google.github.io/mediapipe/](https://github.com/google-ai-edge/mediapipe)) to let users draw on the screen using only their fingers — no mouse or touchscreen needed!

- The script uses MediaPipe Hands to detect and track the user's hand landmarks in real time.
- Specific finger gestures are mapped to actions:
  - Index finger extended = Drawing mode
  - Both index and middle fingers extended = Selection mode (change color/tool)
- A virtual canvas is overlaid on the video feed where drawings appear as you move your hand.

Tech Stack

- Python 3.11
- OpenCV for video processing
- MediaPipe for hand detection and tracking
- NumPy for canvas operations
