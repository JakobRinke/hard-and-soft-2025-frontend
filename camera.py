import cv2
import requests
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.stream_url = "http://localhost:8080/stream?topic=/ascamera/camera_publisher/rgb0/image"
        self.stream = requests.get(self.stream_url, stream=True)
        self.bytes = b''

    def __del__(self):
        self.stream.close()

    def get_frame(self):
        try:
            # Lies kontinuierlich den Stream Buffer
            self.bytes += self.stream.raw.read(1024)
            a = self.bytes.find(b'\xff\xd8')  # JPEG start
            b = self.bytes.find(b'\xff\xd9')  # JPEG end
            if a != -1 and b != -1:
                jpg = self.bytes[a:b+2]
                self.bytes = self.bytes[b+2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    resized_image = cv2.resize(img, (160, 120))
                    ret, jpeg = cv2.imencode('.jpg', resized_image)
                    return jpeg.tobytes()
                else:
                    print("?? Bild konnte nicht dekodiert werden.")
                    return b''
            else:
                print("?? Noch kein vollständiges JPEG-Paket.")
                return b''
        except Exception as e:
            print(f"?? Fehler beim Lesen des MJPEG Streams: {e}")
            return b''
