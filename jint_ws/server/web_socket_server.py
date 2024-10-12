import websockets
import asyncio
import base64
import pandas as pd
from datetime import datetime
import json
from video_capture import VideoCapture
from emotion_detector import EmotionDetector
import cv2

class WebSocketServer:
    def __init__(self):
        self.video_capture = VideoCapture()
        self.emotion_detector = EmotionDetector()
        self.emotion_data_df = pd.DataFrame(columns=['timestamp', 'sad', 'angry', 'surprise', 'fear', 'happy', 'disgust', 'neutral'])

    async def video_stream(self, websocket, path):
        try:
            while True:
                frame = self.video_capture.get_frame()
                if frame is None:
                    break

                faces = self.video_capture.detect_faces(frame)
                for (x, y, w, h) in faces:
                    face_roi = frame[y:y + h, x:x + w]

                    emotions, dominant_emotion = self.emotion_detector.analyze_emotion(face_roi)
                    if emotions is None:
                        continue

                    confidence_level = emotions[dominant_emotion] if dominant_emotion in emotions else 0
                    self.emotion_detector.draw_emotion(frame, (x, y, w, h), dominant_emotion, confidence_level)

                    # Append the emotion data to the DataFrame
                    new_row = pd.DataFrame([{
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'sad': emotions.get('sad', 0),
                        'angry': emotions.get('angry', 0),
                        'surprise': emotions.get('surprise', 0),
                        'fear': emotions.get('fear', 0),
                        'happy': emotions.get('happy', 0),
                        'disgust': emotions.get('disgust', 0),
                        'neutral': emotions.get('neutral', 0)
                    }])
                    self.emotion_data_df = pd.concat([self.emotion_data_df, new_row], ignore_index=True)

                    # Convert the frame to JPEG for WebSocket transmission
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_data = base64.b64encode(buffer).decode('utf-8')

                    # Prepare emotion data to be sent over WebSocket
                    emotions_json = {
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'sad': emotions.get('sad', 0),
                        'angry': emotions.get('angry', 0),
                        'surprise': emotions.get('surprise', 0),
                        'fear': emotions.get('fear', 0),
                        'happy': emotions.get('happy', 0),
                        'disgust': emotions.get('disgust', 0),
                        'neutral': emotions.get('neutral', 0)
                    }

                    # Send both frame and emotion data as a JSON string
                    message = json.dumps({'frame': frame_data, 'emotions': emotions_json})
                    await websocket.send(message)

                # Display the frame locally
                cv2.imshow('Real-time Emotion Detection', frame)

                # Press 'q' to exit the video capture
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                await asyncio.sleep(0.1)  # Adjust the frame rate

                # Save the emotion data to a CSV file after every frame
                self.emotion_data_df.to_csv('emotion_data.csv', index=False)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")

        finally:
            # Release the camera and close windows when done
            self.video_capture.release()

    def start_server(self):
        start_server = websockets.serve(self.video_stream, 'localhost', 8080)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
