from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import asyncio
import websockets
import base64
import pandas as pd
from datetime import datetime
import json
import cv2

# Import custom modules for video capture, emotion detection, and transcription
from video_capture import VideoCapture
from emotion_detector import EmotionDetector
from transcriber import Transcriber  # If available, otherwise comment this out

app = Flask(__name__)
CORS(app)

# Flask threading variables
thread = None
thread_running = False

# WebSocket server class
class WebSocketServer:
    def __init__(self):
        self.video_capture = VideoCapture()
        self.emotion_detector = EmotionDetector()
        # self.transcriber = Transcriber(output_csv="transcription.csv", interval=5)  # Uncomment if available

        # Initialize emotion data DataFrame
        self.emotion_data_df = pd.DataFrame(columns=['timestamp', 'sad', 'angry', 'surprise', 'fear', 'happy', 'disgust', 'neutral', 'transcript'])
        self.prev_transcript = ""
        self.out_transcript = ""

    async def video_stream(self, websocket, path):
        try:
            while True:
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

                # Prepare timestamp and retrieve the latest transcript (if Transcriber is used)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                    break

                await asyncio.sleep(0.1)  # Adjust the frame rate

                # Save the emotion data to a CSV file after every frame
                self.emotion_data_df.to_csv('emotion_data.csv', index=False)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
        finally:
            self.video_capture.release()

    def start_server(self):
        """Starts the WebSocket server."""
        start_server = websockets.serve(self.video_stream, 'localhost', 8080)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

# Flask route to start the WebSocket server
@app.route('/start-thread', methods=['POST'])
def start_thread():
    global thread, thread_running
    if not thread_running:
        thread_running = True
        # Start the WebSocket server in a separate thread
        websocket_server = WebSocketServer()
        thread = threading.Thread(target=websocket_server.start_server)
        thread.start()
        return jsonify({"status": f"Thread started "}), 200
    else:
        return jsonify({"status": "Thread is already running"}), 200

@app.route('/stop-thread', methods=['POST'])
def stop_thread():
    global thread_running
    if thread_running:
        thread_running = False
        return jsonify({"status": "Thread stopped"}), 200
    else:
        return jsonify({"status": "No thread is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
