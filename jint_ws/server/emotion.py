import cv2
from deepface import DeepFace
import asyncio
import websockets
import base64
import pandas as pd
from datetime import datetime
import json

async def video_stream(websocket, path):
    try:
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

            # Initialize emotion values
            sad = angry = surprise = fear = happy = disgust = neutral = 0

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Extract the face ROI (Region of Interest)
                face_roi = rgb_frame[y:y + h, x:x + w]

                try:
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

                    # Draw rectangle around face and label with predicted dominant emotion
                    dominant_emotion = result[0]['dominant_emotion']
                    confidence_level = emotion_confidences[dominant_emotion]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, f"{dominant_emotion} ({confidence_level:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                except Exception as e:
                    print(f"Error during emotion analysis: {e}")
                    # Set all emotion values to 0 if analysis fails
                    sad = angry = surprise = fear = happy = disgust = neutral = 0

            # Append the emotion data to the DataFrame using pandas concat
            new_row = pd.DataFrame([{
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'sad': sad,
                'angry': angry,
                'surprise': surprise,
                'fear': fear,
                'happy': happy,
                'disgust': disgust,
                'neutral': neutral
            }])
            emotion_data_df = pd.concat([emotion_data_df, new_row], ignore_index=True)

            # Convert the frame to JPEG for WebSocket transmission
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')

            # Prepare emotion data to be sent over WebSocket
            emotions = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'sad': sad,
                'angry': angry,
                'surprise': surprise,
                'fear': fear,
                'happy': happy,
                'disgust': disgust,
                'neutral': neutral
            }

            # Send both frame and emotion data as a JSON string
            message = json.dumps({'frame': frame_data, 'emotions': emotions})
            await websocket.send(message)

            # Display the frame locally
            cv2.imshow('Real-time Emotion Detection', frame)

            # Press 'q' to exit the video capture
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            await asyncio.sleep(0.1)  # Adjust the frame rate

            # Save the emotion data to a CSV file after every frame
            emotion_data_df.to_csv('emotion_data.csv', index=False)

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")

    finally:
        # Release the camera and close windows when done
        cap.release()
        cv2.destroyAllWindows()

# Start the WebSocket server
start_server = websockets.serve(video_stream, 'localhost', 8080)

# Run the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
