import cv2
import numpy as np
import urllib.request

class VideoCamera(object):
    def __init__(self):
        self.stream_url = "http://localhost:8080/stream?topic=/ascamera/camera_publisher/rgb0/image"
        self.stream = urllib.request.urlopen(self.stream_url)
        self.bytes = b''

    def __del__(self):
        self.stream.close()

    def get_frame(self):
        try:
            while True:
                self.bytes += self.stream.read(1024)
                start = self.bytes.find(b'\xff\xd8')
                end = self.bytes.find(b'\xff\xd9')

                if start != -1 and end != -1 and end > start:
                    jpg = self.bytes[start:end+2]
                    self.bytes = self.bytes[end+2:]  # Rest behalten, evtl. nächstes Bild schon teilweise da
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if img is not None:
                        resized_image = cv2.resize(img, (160, 120))
                        ret, jpeg = cv2.imencode('.jpg', resized_image)
                        return jpeg.tobytes()
                    else:
                        print("⚠️ Fehler beim Dekodieren des Bildes.")
                        return b''
                # Andernfalls einfach weiter lesen bis genug Daten da sind

        except Exception as e:
            print(f"⚠️ Fehler beim Lesen des MJPEG Streams: {e}")
            return b''
