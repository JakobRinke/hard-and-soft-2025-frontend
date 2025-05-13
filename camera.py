import requests
MJPEG_STREAM_URL = "http://localhost:8080/stream?topic=/ascamera/camera_publisher/rgb0/image"

def generate():
    with requests.get(MJPEG_STREAM_URL, stream=True) as r:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                yield chunk
