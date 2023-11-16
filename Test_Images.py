import streamlit as st
import cv2
import numpy as np
import webbrowser
from keras.models import model_from_json

def load_emotion_model():
    # Load the emotion model from JSON and weights
    json_file = open('C:/Users/chenn/OneDrive/Desktop/MUSIC_PLAYER/validate/emotion_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)
    emotion_model.load_weights('C:/Users/chenn/OneDrive/Desktop/MUSIC_PLAYER/validate/emotion_model.h5')
    return emotion_model
emotion_model = load_emotion_model()

emotion_dict = {0: "Angry", 1: "Fearful", 2: "Happy", 3: "Neutral", 4: "Sad", 5: "Surprised"}

def detect_emotion(frame, emotion_model):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    face_cascade = cv2.CascadeClassifier('C:/Users/chenn/OneDrive/Desktop/MUSIC_PLAYER/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process each detected face
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Extract the face region
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_gray_resized = cv2.resize(roi_gray, (48, 48))
        roi_gray_normalized = roi_gray_resized / 255.0
        roi_gray_reshaped = np.reshape(roi_gray_normalized, (1, 48, 48, 1))

        # Predict emotion using the loaded model directly
        emotion_prediction = emotion_model.predict(roi_gray_reshaped)
        maxindex = int(np.argmax(emotion_prediction))
        emotion_label = emotion_dict[maxindex]

        # Display the emotion label near the face
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Return maxindex for later use
        return maxindex

    return None  # Return None if no face detected

def emotion():
    st.header("Provide Preferences To Recommender Music....,")


    Singer = st.text_input("Enter Singer Name")
    Language = st.text_input("Enter Language")

    run = st.button('Start')
    stop = st.button('Stop Video')

    button1 = st.button('Go to YouTube')
    button2 = st.button('Go to Spotify') # New button for redirection
    redirect_triggered = False  # Flag to track if redirection has been triggered
    stop_flag = False  # Flag to stop video capture

    # Load the emotion detection model
    emotion_model = load_emotion_model()

    # Initialize video capture
    camera = cv2.VideoCapture(0)

    maxindex = None  # Initialize maxindex

    if run:
        st.title("Wait for emotion Capture")
        FRAME_WINDOW = st.image([])
        while run and not stop_flag:
            ret, frame = camera.read()
            if not ret:
                break

            # Detect emotion in the frame
            result = detect_emotion(frame, emotion_model)
            if result:
                maxindex = result

            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame
            FRAME_WINDOW.image(frame_rgb, channels='RGB')

            # If both inputs are provided and emotion is detected
            if Language and Singer and maxindex is not None:
                emotion_label = emotion_dict[maxindex]  # Get the emotion label

                # Display the emotion label on the video
                cv2.putText(frame, emotion_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if button1 and not redirect_triggered:
                webbrowser.open(f"https://www.youtube.com/results?search_query={Language}+{Singer}+{emotion_label}+songs+playlist")
                redirect_triggered = True  # Set the flag to True to prevent further redirections
                stop_flag = True  # Stop the video when redirection occurs

            if button2 and not redirect_triggered:
                webbrowser.open(f"https://open.spotify.com/search/{Language}%20{Singer}%20{emotion_label}%20songs%20playlist")
                redirect_triggered = True  # Set the flag to True to prevent further redirections
                stop_flag = True  # Stop the video when redirection occurs

            # Release the camera when "Stop" is pressed or after redirection
            if stop or stop_flag:
                run = False
                camera.release()
                stop_flag = True

    return None

if __name__ == "__main__":
    emotion()