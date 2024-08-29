# Gesture-Controlled Interface using MediaPipe

## Overview

This project leverages the power of **MediaPipe** to implement a comprehensive gesture-controlled interface. By utilizing MediaPipe's advanced tracking capabilities, this project provides functionalities such as face mesh detection, hand movement detection, holistic tracking, object detection with 3D bounding boxes (Objectron), pose estimation, and gesture-based controls including a virtual keyboard and system volume control.

## Features

### 1. Face Mesh Detection
- **Description:** This module detects and tracks facial landmarks in real-time, enabling applications such as facial recognition, emotion detection, and more.
- **Usage:** The face mesh is detected using MediaPipe's face mesh solution, providing high-fidelity tracking even under challenging conditions.

### 2. Hand Movement Detection
- **Description:** Detects and tracks 21 hand landmarks per hand, allowing for precise hand gesture recognition.
- **Usage:** Ideal for gesture-based controls, sign language recognition, and other interactive applications.

### 3. Holistic Tracking
- **Description:** Combines face mesh, hand tracking, and pose estimation to provide a full-body tracking solution. This holistic approach enables more complex interactions, such as body gesture control.
- **Usage:** Used in scenarios where the coordination of face, hand, and body movements are needed, such as in virtual environments and gaming.

### 4. Object Detection (Objectron)
- **Description:** Detects objects in real-time and provides a 3D bounding box around them. This feature can be used for object recognition, augmented reality applications, and more.
- **Usage:** The Objectron module is used for detecting common objects like cups, chairs, and more with depth estimation.

### 5. Pose Estimation
- **Description:** Tracks 33 key body landmarks to estimate human pose. This feature is essential for fitness applications, animation, and body movement analysis.
- **Usage:** Can be utilized in workout applications to correct postures or in animations where human motion capture is needed.

### 6. Virtual Keyboard using Gestures
- **Description:** A virtual keyboard that is controlled entirely by hand gestures. This feature allows users to type without physically touching a keyboard, ideal for touchless interfaces.
- **Usage:** The virtual keyboard uses hand tracking to detect gestures and map them to keyboard inputs.

### 7. Windows Volume Control using Gestures
- **Description:** Adjust the system volume on a Windows machine using hand gestures. This feature allows for hands-free volume control.
- **Usage:** By detecting specific gestures, the system can increase, decrease, or mute the volume, enhancing the user experience in media applications.

## Installation

### Prerequisites
- Python 3.8 or higher
- MediaPipe
- OpenCV
- Numpy
- PyAutoGUI (for Windows volume control)
- PyGetWindow (for managing window focus)

```bash
pip install mediapipe opencv-python numpy pyautogui pygetwindow
```

### Clone the repository:
   ```bash
   git clone https://github.com/AvI-Grigzy/Gesture-Controlled-Interface-using-MediaPipe.git
   ```
## Running the Program

Once you have installed all the necessary dependencies, you can run the various components of this project. Each component is designed to perform specific tasks, such as detecting facial landmarks, tracking hand movements, or controlling system volume using gestures. 
