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
        self.transcriber = Transcriber(output_csv="jint_ws/server/transcription.csv", interval=5)  # Initialize Transcriber

        # Start the transcription in a separate thread
        self.transcription_thread = threading.Thread(target=self.transcriber.start_transcription)
        self.transcription_thread.daemon = True  # Daemonize thread
        self.transcription_thread.start()

        self.emotion_data_df = pd.DataFrame(columns=['timestamp', 'sad', 'angry', 'surprise', 'fear', 'happy', 'disgust', 'neutral', 'transcript'])

        self.prev_transcript = ""
        self.out_transcript = ""
        self.keep_running = False

    async def video_stream(self, websocket, path):
        try:
            while self.keep_running:
                frame = self.video_capture.get_frame()
                if frame is None:
                    break

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

                # Prepare timestamp and retrieve the latest transcript
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                latest_transcript = self.transcriber.get_latest_transcript()  # Ensure you have this method in your Transcriber
                if(self.prev_transcript == latest_transcript):
                    self.out_transcript = ""
                else: 
                    self.out_transcript = latest_transcript

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
                        'neutral': emotions.get('neutral', 0),
                        'transcript': self.out_transcript  # Include transcript here
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
                        'neutral': 0,
                        'transcript': self.out_transcript  # Include transcript even if no dominant emotion
                    }

                # Append the emotion data to the DataFrame
                new_row = pd.DataFrame([emotions_json])
                self.emotion_data_df = pd.concat([self.emotion_data_df, new_row], ignore_index=True)

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
                    self.stop_server()
                    break

                await asyncio.sleep(0.1)  # Adjust the frame rate

                # Save the emotion data to a CSV file after every frame
                self.emotion_data_df.to_csv('jint_ws/server/emotion_data.csv', index=False)

                self.prev_transcript = latest_transcript

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")

        finally:
            # Release the camera and close windows when done
            self.video_capture.release()

    def start_server(self):
        """Starts the WebSocket server."""
        self.keep_running = True
        self.transcriber.start_running()
        start_server = websockets.serve(self.video_stream, 'localhost', 8080)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def stop_server(self):
        self.keep_running = False
        self.transcriber.stop_running()
        asyncio.get_event_loop().stop()


