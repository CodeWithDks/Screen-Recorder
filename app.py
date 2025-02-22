from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import threading
from recorder import ScreenRecorder

app = Flask(__name__)
CORS(app)

recorder = ScreenRecorder()

@app.route("/start", methods=["POST"])
def start_recording():
    recorder.start()
    return jsonify({"message": "Recording started"}), 200

@app.route("/pause", methods=["POST"])
def pause_recording():
    recorder.pause()
    return jsonify({"message": "Recording paused"}), 200

@app.route("/resume", methods=["POST"])
def resume_recording():
    recorder.resume()
    return jsonify({"message": "Recording resumed"}), 200

@app.route("/stop", methods=["POST"])
def stop_recording():
    file_path = recorder.stop()
    return jsonify({"message": "Recording stopped", "file_path": file_path}), 200

@app.route("/download", methods=["GET"])
def download_video():
    return send_file("recorded_video.avi", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
