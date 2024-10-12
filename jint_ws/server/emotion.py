import cv2
from deepface import DeepFace
import asyncio
import websockets
import base64
import pandas as pd
from datetime import datetime

async def video_stream(websocket, path):
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Start capturing video
    cap = cv2.VideoCapture(0)

    # Create a DataFrame to store emotion data with specific columns
    emotion_data_df = pd.DataFrame(columns=['timestamp', 'sad', 'angry', 'surprise', 'fear', 'happy', 'disgust', 'neutral'])

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale frame to RGB format
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Extract the face ROI (Region of Interest)
            face_roi = rgb_frame[y:y + h, x:x + w]

            # Perform emotion analysis on the face ROI
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

            # Get emotion confidences
            emotion_confidences = result[0]['emotion']

            # Extract the emotions and corresponding confidence levels
            sad = emotion_confidences.get('sad', 0)
            angry = emotion_confidences.get('angry', 0)
            surprise = emotion_confidences.get('surprise', 0)
            fear = emotion_confidences.get('fear', 0)
            happy = emotion_confidences.get('happy', 0)
            disgust = emotion_confidences.get('disgust', 0)
            neutral = emotion_confidences.get('neutral', 0)

            # Append the emotion data to the DataFrame
            emotion_data_df = emotion_data_df.append({
                'timestamp': datetime.now(),
                'sad': sad,
                'angry': angry,
                'surprise': surprise,
                'fear': fear,
                'happy': happy,
                'disgust': disgust,
                'neutral': neutral
            }, ignore_index=True)

            # Draw rectangle around face and label with predicted dominant emotion
            dominant_emotion = result[0]['dominant_emotion']
            confidence_level = emotion_confidences[dominant_emotion]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"{dominant_emotion} ({confidence_level:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')

        # Send the frame data via WebSocket
        await websocket.send(frame_data)

        # Display the resulting frame
        cv2.imshow('Real-time Emotion Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        await asyncio.sleep(0.1)  # Adjust the frame rate

        # Save the emotion data to a CSV file after every frame
        emotion_data_df.to_csv('jint_ws/server/emotion_data.csv', index=False)

    cap.release()
    cv2.destroyAllWindows()

start_server = websockets.serve(video_stream, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
