import cv2
import requests
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.stream_url = "http://localhost:8080/stream?topic=/ascamera/camera_publisher/rgb0/image"

    def __del__(self):
        self.video.release()

    def get_frame(self):
        try:
            # Try to fetch the frame from the stream URL
            response = requests.get(self.stream_url, stream=True, timeout=1)
            if response.status_code == 200:
                data = np.frombuffer(response.content, np.uint8)
                image = cv2.imdecode(data, cv2.IMREAD_COLOR)
                if image is not None:
                    resized_image = cv2.resize(image, (160, 120))  # Resize to 160x120
                    ret, jpeg = cv2.imencode('.jpg', resized_image)
                    return jpeg.tobytes()
        except Exception:
            pass  # Fallback to video capture if the stream fails

        # Fallback to video capture
        if not self.video.isOpened():
            self.video.open(0)
        cv2.setLogLevel(0)

        success, image = self.video.read()
        if not success:
            return b''  # Return empty bytes instead of None
        else:
            resized_image = cv2.resize(image, (160, 120))  # Resize to 160x120
            ret, jpeg = cv2.imencode('.jpg', resized_image)
            return jpeg.tobytes()