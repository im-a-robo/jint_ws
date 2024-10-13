import websockets
import asyncio
import base64
import pandas as pd
from datetime import datetime
import json
from video_capture import VideoCapture
from emotion_detector import EmotionDetector
from transcriber import Transcriber  # Ensure you have this import
import cv2
import threading

class WebSocketServer:
    def __init__(self):
        self.video_capture = VideoCapture()
        self.emotion_detector = EmotionDetector()
        self.transcriber = Transcriber(output_csv="jint_ws/server/combined_data.csv", interval=5)  # Use combined CSV
        
        # Start the transcription in a separate thread
        self.transcription_thread = threading.Thread(target=self.transcriber.start_transcription)
        self.transcription_thread.daemon = True  # Daemonize thread
        self.transcription_thread.start()

        # Create a DataFrame to hold emotion data
        self.emotion_data_df = pd.DataFrame(columns=['timestamp', 'sad', 'angry', 'surprise', 'fear', 'happy', 'disgust', 'neutral'])

    async def video_stream(self, websocket, path):
        try:
            while True:
                frame = self.video_capture.get_frame()
                if frame is None:
                    break

                # Prepare the timestamp at the beginning of each frame processing
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                faces = self.video_capture.detect_faces(frame)
                emotions = {}
                dominant_emotion = None

                # Process faces for emotion detection
                for (x, y, w, h) in faces:
                    face_roi = frame[y:y + h, x:x + w]
                    emotions, dominant_emotion = self.emotion_detector.analyze_emotion(face_roi)

                    if emotions is None:
                        continue

                    confidence_level = emotions[dominant_emotion] if dominant_emotion in emotions else 0
                    self.emotion_detector.draw_emotion(frame, (x, y, w, h), dominant_emotion, confidence_level)

                    # Prepare emotion data for the DataFrame
                    new_row = {
                        'timestamp': timestamp,
                        'sad': emotions.get('sad', 0),
                        'angry': emotions.get('angry', 0),
                        'surprise': emotions.get('surprise', 0),
                        'fear': emotions.get('fear', 0),
                        'happy': emotions.get('happy', 0),
                        'disgust': emotions.get('disgust', 0),
                        'neutral': emotions.get('neutral', 0)
                    }

                    # Append the new row to the DataFrame using pd.concat
                    new_row_df = pd.DataFrame([new_row])
                    self.emotion_data_df = pd.concat([self.emotion_data_df, new_row_df], ignore_index=True)

                    # Save the new row directly to CSV
                    self.transcriber.save_combined_data(new_row_df)

                # Prepare emotion data to be sent over WebSocket
                if dominant_emotion:
                    emotions_json = {
                        'timestamp': timestamp,
                        'sad': emotions.get('sad', 0),
                        'angry': emotions.get('angry', 0),
                        'surprise': emotions.get('surprise', 0),
                        'fear': emotions.get('fear', 0),
                        'happy': emotions.get('happy', 0),
                        'disgust': emotions.get('disgust', 0),
                        'neutral': emotions.get('neutral', 0)
                    }
                else:
                    emotions_json = {
                        'timestamp': timestamp,
                        'sad': 0,
                        'angry': 0,
                        'surprise': 0,
                        'fear': 0,
                        'happy': 0,
                        'disgust': 0,
                        'neutral': 0
                    }

                # Convert the frame to JPEG for WebSocket transmission
                _, buffer = cv2.imencode('.jpg', frame)
                frame_data = base64.b64encode(buffer).decode('utf-8')

                # Send both frame and emotion data as a JSON string
                message = json.dumps({'frame': frame_data, 'emotions': emotions_json})
                await websocket.send(message)

                # Display the frame locally
                cv2.imshow('Real-time Emotion Detection', frame)

                # Press 'q' to exit the video capture
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                await asyncio.sleep(0.1)  # Adjust the frame rate

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")

        finally:
            # Release the camera and close windows when done
            self.video_capture.release()


    def start_server(self):
        """Starts the WebSocket server."""
        start_server = websockets.serve(self.video_stream, 'localhost', 8080)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()



    def start_server(self):
        """Starts the WebSocket server."""
        start_server = websockets.serve(self.video_stream, 'localhost', 8080)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
