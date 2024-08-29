import cv2
import mediapipe as mp

# This model is specifically designed for detecting 3D objects in real-time. 
# It provides both 2D bounding boxes and 3D bounding boxes around objects like shoes, chairs, cups, and cameras
mp_objectron = mp.solutions.objectron
objectron = mp_objectron.Objectron(static_image_mode=False, max_num_objects=5, min_detection_confidence=0.5, min_tracking_confidence=0.5, model_name='Chair')
#mediapipe
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = objectron.process(rgb_frame)

    if results.detected_objects:
        for detected_object in results.detected_objects:
            mp.solutions.drawing_utils.draw_landmarks(frame, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
            mp.solutions.drawing_utils.draw_axis(frame, detected_object.rotation, detected_object.translation)

    cv2.imshow('Objectron', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
