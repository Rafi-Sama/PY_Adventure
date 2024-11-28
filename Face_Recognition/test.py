import cv2
import face_recognition
from PIL import Image
import numpy as np

# Open the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a single frame of video
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to grab frame")
        continue

    # Ensure the frame is in uint8
    if frame.dtype != "uint8":
        frame = frame.astype("uint8")

    # Convert frame to RGB using OpenCV
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Verify that the frame is in the correct format
    print(f"Frame dtype: {rgb_frame.dtype}, Frame shape: {rgb_frame.shape}")

    try:
        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
    except Exception as e:
        print(f"Error during face detection: {e}")
        continue

    # Loop through each detected face and draw a rectangle around it
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the frame with rectangles drawn around faces
    cv2.imshow("Video", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
