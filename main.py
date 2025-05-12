from flask import Flask, render_template, redirect, url_for, request
import web_auth
from datetime import datetime
import data

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



if __name__ == "__main__":
  app.run()