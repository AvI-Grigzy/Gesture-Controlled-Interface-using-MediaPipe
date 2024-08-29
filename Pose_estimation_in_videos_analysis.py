import cv2
import mediapipe as mp

# Initialize Mediapipe holistic class
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

# Initialize Mediapipe drawing class
mp_drawing = mp.solutions.drawing_utils

# Initialize Mediapipe face mesh class
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Define a subset of landmark indices to visualize
key_landmark_indices = [
    10,  # Mid-point of the forehead
    234, 454,  # Left and right temple
    61, 291,  # Left and right mouth corner
    1,  # Chin
    199, 429,  # Left and right cheekbone
    33, 263,  # Left and right eye outer corner
    133, 362,  # Left and right eye inner corner
    168,  # Nose tip
]

# Define the indices for the facial boundary (contour)
facial_boundary_indices = [
    10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379,
    378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162,
    21, 54, 103, 67, 109
]

# Open video file instead of webcam
video_path = 'input_video.mp4' # update the video file location here 
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(rgb_frame)

    # Draw face landmarks
    if results.face_landmarks:
        ih, iw, _ = frame.shape
        face_landmarks = results.face_landmarks

        # Draw the facial boundary
        for i in range(len(facial_boundary_indices) - 1):
            start_idx = facial_boundary_indices[i]
            end_idx = facial_boundary_indices[i + 1]
            start_landmark = face_landmarks.landmark[start_idx]
            end_landmark = face_landmarks.landmark[end_idx]
            start_x, start_y = int(start_landmark.x * iw), int(start_landmark.y * ih)
            end_x, end_y = int(end_landmark.x * iw), int(end_landmark.y * ih)
            cv2.line(frame, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)  # Blue boundary lines

        # Draw the key landmarks
        for idx in key_landmark_indices:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * iw), int(landmark.y * ih)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Green dots

    # Draw left hand landmarks
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    
    # Draw right hand landmarks
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    
    # Draw pose landmarks
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

    cv2.imshow('Holistic Tracking', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
