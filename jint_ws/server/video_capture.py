import cv2

class VideoCapture:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def get_frame(self):
        """Captures and returns a frame from the webcam."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def detect_faces(self, frame):
        """Detects faces in the provided frame."""
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def release(self):
        """Releases the video capture object."""
        self.cap.release()
        cv2.destroyAllWindows()
