from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os
import time
import asyncio

from api.modules.track_record import handle_track_recording

app = Flask(__name__)
CORS(app)

last_track_info = ""
last_track_timestamp = 0
database_path = os.path.join("track_database", "database.txt")

async def loop_track_recording():
    while True:
        await asyncio.sleep(12)
        await handle_track_recording()

@app.route('/api/track_id', methods=['GET', 'OPTIONS'])
def get_track():
    global last_track_info
    global last_track_timestamp

    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    track_data = get_latest_track_info()
    
    if last_track_info:
        if track_data != last_track_info:
            last_track_info = track_data
            last_track_timestamp = time.time()
            print("app.py:", track_data)
            return jsonify(track_data), 200
        else:
            current_timestamp = time.time()
            time_diff = current_timestamp - last_track_timestamp
            if time_diff <= 60:
                print("app.py:", track_data)
                return jsonify(track_data), 200
            else:
                print("app.py:", "Yup!")
                return "No recent tracks found.", 204
    else:
        print("app.py:", "Hell yeah 4!")
        return "No recent tracks found.", 204

def get_latest_track_info():
    with open(database_path, "r") as file:
        lines = file.readlines()
        if lines:
            latest_track = lines[-1].strip()
            timestamp, title_subtitle = latest_track.split(" | ")
            title, subtitle = title_subtitle.split(" - ")

            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            twelve_seconds_ago = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() - 12))

            if timestamp > twelve_seconds_ago:
                print(f"{title} - {subtitle}")
                return f"{title} - {subtitle}"

        return ""

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(loop_track_recording())
    app.run(host='localhost', port=5000, debug=True)
