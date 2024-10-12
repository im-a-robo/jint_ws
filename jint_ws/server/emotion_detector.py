import cv2
from deepface import DeepFace

class EmotionDetector:
    def __init__(self):
        pass

    def analyze_emotion(self, face_roi):
        """Analyzes emotions of the provided face ROI (Region of Interest)."""
        try:
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            return result[0]['emotion'], result[0]['dominant_emotion']
        except Exception as e:
            print(f"Error during emotion analysis: {e}")
            return None, None

    def draw_emotion(self, frame, face_coordinates, dominant_emotion, confidence_level):
        """Draws a rectangle around the face and the dominant emotion on the frame."""
        x, y, w, h = face_coordinates
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, f"{dominant_emotion} ({confidence_level:.2f})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
