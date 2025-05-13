import cv2

class VideoCamera(object):
    def __init__(self):
        # Versuche direkt den MJPEG Stream zu öffnen
        self.stream_url = "http://localhost:8080/stream?topic=/ascamera/camera_publisher/rgb0/image"
        self.video = cv2.VideoCapture(self.stream_url)
        if not self.video.isOpened():
            print("⚠️ Stream konnte nicht geöffnet werden, versuche lokale Kamera...")
            self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        cv2.setLogLevel(0)
        success, image = self.video.read()
        if not success:
            print("⚠️ Kein Bild empfangen!")
            return b''
        resized_image = cv2.resize(image, (160, 120))
        ret, jpeg = cv2.imencode('.jpg', resized_image)
        return jpeg.tobytes()
