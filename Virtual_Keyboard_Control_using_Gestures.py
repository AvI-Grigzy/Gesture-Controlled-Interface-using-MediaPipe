import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize Mediapipe hands class
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize Mediapipe drawing class
mp_drawing = mp.solutions.drawing_utils

# Define a function to recognize specific gestures
def recognize_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Simple gesture: if thumb and index fingertips are close, return "Select"
    if np.linalg.norm([thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y, thumb_tip.z - index_tip.z]) < 0.05:
        return "Select"
    # If index finger is up and others are down, return "Type"
    if index_tip.y < middle_tip.y and index_tip.y < ring_tip.y and index_tip.y < pinky_tip.y:
        return "Type"
    return None

# Define a function to draw the virtual keyboard
def draw_virtual_keyboard(frame):
    keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    for i, key in enumerate(keys):
        if key == " ":
            x = 300
            y = 250
            cv2.rectangle(frame, (x, y), (x + 200, y + 60), (255, 0, 0), 2)
            cv2.putText(frame, "SPACE", (x + 50, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            x = (i % 10) * 70 + 50
            y = (i // 10) * 70 + 50
            cv2.rectangle(frame, (x, y), (x + 60, y + 60), (255, 0, 0), 2)
            cv2.putText(frame, key, (x + 20, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return keys

# Define a function to check if a point is within a rectangle
def is_point_in_rect(x, y, rect_x, rect_y, rect_width, rect_height):
    return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

frame_num = 0
gesture_confirm_frame_count = 0  # Counter to confirm the gesture
gesture_confirm_threshold = 20  # Increase the number of frames to confirm the gesture
message_display_frames = 50  # Number of frames to display the message
message_display_counter = 0  # Counter to track message display duration
message = ""  # Message to display on the screen
message_shown = False  # Flag to track if the message has already been displayed
hand_last_seen = time.time()  # Timestamp of when the hand was last seen
delay_seconds = 2  # Delay in seconds before showing the message when hand re-enters the frame
last_key_pressed_time = 0  # Time of the last key press to debounce key presses
debounce_delay = 1  # Delay in seconds to wait for the next key press

collected_text = ""  # String to collect the selected keys

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Ignoring empty camera frame.")
        continue
    
    # Convert the image from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect the hands
    result = hands.process(rgb_frame)
    
    # Draw the virtual keyboard
    keys = draw_virtual_keyboard(frame)
    
    # Draw the hand annotations on the image
    if result.multi_hand_landmarks:
        hand_last_seen = time.time()  # Update the timestamp when hand is seen
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Recognize gestures and display on the screen
            gesture = recognize_gesture(hand_landmarks)
            if gesture == "Select":
                gesture_confirm_frame_count += 1
                if gesture_confirm_frame_count >= gesture_confirm_threshold:
                    current_time = time.time()
                    if current_time - last_key_pressed_time > debounce_delay:
                        last_key_pressed_time = current_time
                        message = "Select Gesture Detected"
                        message_display_counter = message_display_frames
                        message_shown = True  # Set flag to indicate message has been shown
                        gesture_confirm_frame_count = 0  # Reset counter after confirmation

                        # Check if the select gesture is over a key
                        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        x_pixel = int(index_finger_tip.x * frame.shape[1])
                        y_pixel = int(index_finger_tip.y * frame.shape[0])
                        for i, key in enumerate(keys):
                            if key == " ":
                                key_x, key_y, key_width, key_height = 300, 250, 200, 60
                            else:
                                key_x = (i % 10) * 70 + 50
                                key_y = (i // 10) * 70 + 50
                                key_width, key_height = 60, 60
                            if is_point_in_rect(x_pixel, y_pixel, key_x, key_y, key_width, key_height):
                                if key == " ":
                                    key = "SPACE"
                                    collected_text += " "
                                else:
                                    collected_text += key
                                print(collected_text)
                                break
            else:
                gesture_confirm_frame_count = 0
            
            if message_display_counter > 0:
                cv2.putText(frame, message, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
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
