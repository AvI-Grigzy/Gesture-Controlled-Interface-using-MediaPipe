import cv2
import mediapipe as mp
import csv

# Initialize Mediapipe hands class
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize Mediapipe drawing class
mp_drawing = mp.solutions.drawing_utils

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

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
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract and write the hand landmarks data to the CSV file
            row = [frame_num]
            for hand_landmarks in result.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    row += [landmark.x, landmark.y, landmark.z]
            # If only one hand is detected, pad the row with None for the second hand's landmarks
            if len(result.multi_hand_landmarks) == 1:
                row += [None] * (21 * 3)
            writer.writerow(row)
        
        # Display the output
        cv2.imshow('Hand Tracking', frame)
        
        frame_num += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
