import urllib.request
MJPEG_STREAM_URL = "http://localhost:8080/stream?topic=/ascamera/camera_publisher/rgb0/image"

def generate():
    try:
        with urllib.request.urlopen(MJPEG_STREAM_URL) as stream:
            while True:
                chunk = stream.read(1024)
                if not chunk:
                    break
                yield chunk
    except Exception as e:
        print(f"❌ Fehler im MJPEG Proxy: {e}")