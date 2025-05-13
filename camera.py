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
                    self.bytes = self.bytes[end+2:]  # Buffer aufräumen
                    return jpg  # ? Direkt das JPEG-Bytearray zurückgeben ? ohne Modifikation
        except Exception as e:
            print(f"?? Fehler beim Lesen des MJPEG Streams: {e}")
            return b''
