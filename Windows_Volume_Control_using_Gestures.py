import cv2
import mediapipe as mp
import csv
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time

# Initialize Mediapipe hands class
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize Mediapipe drawing class
mp_drawing = mp.solutions.drawing_utils

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Get the audio device and volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Define a function to recognize specific gestures
def recognize_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    if thumb_tip.y < thumb_ip.y < thumb_mcp.y and thumb_tip.y < index_mcp.y:
        return "Thumbs Up"
    if thumb_tip.y > thumb_ip.y > thumb_mcp.y and thumb_tip.y > index_mcp.y:
        return "Thumbs Down"
    return None

# Open the CSV file for writing
with open('hand_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    header = ['frame']
    for hand_idx in range(2):  # Up to two hands
        for landmark_idx in range(21):  # There are 21 landmarks in a hand
            header += [
                f'x_hand{hand_idx}_landmark{landmark_idx}', 
                f'y_hand{hand_idx}_landmark{landmark_idx}', 
                f'z_hand{hand_idx}_landmark{landmark_idx}'
            ]
    writer.writerow(header)

    frame_num = 0
    volume_control_active = False  # To track if volume control mode is active
    gesture_confirm_frame_count_up = 0  # Counter to confirm the "thumbs up" gesture
    gesture_confirm_frame_count_down = 0  # Counter to confirm the "thumbs down" gesture
    gesture_confirm_threshold = 20  # Increase the number of frames to confirm the gesture
    message_display_frames = 50  # Number of frames to display the message
    message_display_counter = 0  # Counter to track message display duration
    message = ""  # Message to display on the screen
    message_shown = False  # Flag to track if the message has already been displayed
    hand_last_seen = time.time()  # Timestamp of when the hand was last seen
    delay_seconds = 2  # Delay in seconds before showing the message when hand re-enters the frame
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print("Ignoring empty camera frame.")
            continue
        
        # Convert the image from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect the hands
        result = hands.process(rgb_frame)
        
        # Draw the hand annotations on the image
        if result.multi_hand_landmarks:
            hand_last_seen = time.time()  # Update the timestamp when hand is seen
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Recognize gestures and display on the screen
                gesture = recognize_gesture(hand_landmarks)
                if gesture == "Thumbs Up":
                    gesture_confirm_frame_count_up += 1
                    gesture_confirm_frame_count_down = 0
                    if gesture_confirm_frame_count_up >= gesture_confirm_threshold:
                        volume_control_active = True
                        gesture_confirm_frame_count_up = 0  # Reset counter after confirmation
                        message = "Volume Control Activated"
                        message_display_counter = message_display_frames
                        message_shown = True  # Set flag to indicate message has been shown
                elif gesture == "Thumbs Down":
                    gesture_confirm_frame_count_down += 1
                    gesture_confirm_frame_count_up = 0
                    if gesture_confirm_frame_count_down >= gesture_confirm_threshold:
                        volume_control_active = False
                        gesture_confirm_frame_count_down = 0  # Reset counter after confirmation
                        message = "Volume Control Deactivated"
                        message_display_counter = message_display_frames
                        message_shown = True  # Set flag to indicate message has been shown
                else:
                    gesture_confirm_frame_count_up = 0
                    gesture_confirm_frame_count_down = 0
                
                if volume_control_active:
                    # Control the volume using the y-coordinate of the index finger tip
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    volume_level = np.interp(index_finger_tip.y, [0, 1], [-65, 0])  # Map y-coordinate to volume range
                    volume.SetMasterVolumeLevel(volume_level, None)
                
                if message_display_counter > 0:
                    cv2.putText(frame, message, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    message_display_counter -= 1
                    message_shown = False  # Reset the message shown flag
                elif message_shown:
                    message = ""  # Clear the message after it has been displayed for the specified duration
        
        # Check if the hand has re-entered the frame after being absent
        elif time.time() - hand_last_seen >= delay_seconds:
            message_shown = False  # Reset the message shown flag when hand re-enters the frame
        
        # Display the output
        cv2.imshow('Hand Tracking', frame)
        
        frame_num += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
