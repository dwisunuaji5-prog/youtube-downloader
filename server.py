from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Downloader API is running!"

@app.route("/download")
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url tidak ditemukan"}), 400

    id_file = str(uuid.uuid4())
    output_path = f"{id_file}.mp4"

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = send_file(output_path, as_attachment=True)

        # Hapus setelah dikirim
        try:
            os.remove(output_path)
        except:
            pass

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
