from flask import Flask, Response, render_template, redirect, url_for, request
import web_auth
from datetime import datetime
import data
import camera

app = Flask(__name__, static_folder="web/static", template_folder="web/templates")

@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    token = web_auth.check_request(request)
    if token:
        return render_template("home.html", token=token)
    else:
        if request.method == "POST":
            error = "Invalid credentials. Please try again."
    return render_template('login.html', error=error)

@app.route("/data", methods=["GET"])
def get_files():
    token = web_auth.check_request(request)
    if not token:
        return {"error": "Unauthorized"}, 401
    return {
        "data": data.get_data_dir(),
    }


@app.route("/data/<filename>", methods=["GET"])
def get_file(filename):
    token = web_auth.check_request(request)
    if not token:
        return {"error": "Unauthorized"}, 401
    return {
        "data": data.get_data_file(filename),
    }

@app.route("/image/<filename>", methods=["GET"])
def get_image(filename):
    token = web_auth.check_request(request)
    if not token:
        return {"error": "Unauthorized"}, 401
    return data.get_image(filename)

import requests
STREAM_URL = "http://localhost:8080/stream?topic=/ascamera/camera_publisher/rgb0/image"
ORIGINAL_BOUNDARY = b'--boundarydonotcross'
TARGET_BOUNDARY = b'--frame'
@app.route('/video_feed')
def video_feed():
    # Token Check
    token = web_auth.check_request(request)
    if not token:
        return {"error": "Unauthorized"}, 401

    def generate():
        with requests.get(STREAM_URL, stream=True) as r:
            buffer = b''
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    # Patch boundary im Chunk
                    chunk = chunk.replace(ORIGINAL_BOUNDARY, TARGET_BOUNDARY)
                    yield chunk

    return Response(generate(), content_type='multipart/x-mixed-replace; boundary=frame')




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.crt', 'cert.key'))