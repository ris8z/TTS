import os
import time
from threading import Thread

from flask import Flask, abort, render_template, request, send_file

from ttapi import download_video, get_downloadlink

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]

    real_url = get_downloadlink(url)
    if not real_url:
        abort(404, description="Uncorrect Video Link")
    print(real_url)

    file_name = f"{int(time.time())}.mp4"
    download_t = Thread(
        target=download_video, args=(real_url, file_name, DOWNLOAD_FOLDER)
    )
    try:
        download_t.start()
        download_t.join()
    except:
        abort(404, description="Uncorrect Video Link")

    filepath = os.path.join(DOWNLOAD_FOLDER, file_name)
     
    try:
        return send_file(filepath)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    app.run(debug=True)
