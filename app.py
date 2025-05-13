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


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
  app.run(host='0.0.0.0',port='5000')