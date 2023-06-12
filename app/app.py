from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os
import time
import asyncio
import logging
import threading

from api.modules.track_record import handle_track_recording

app = Flask(__name__)
CORS(app)
app.debug = True  # Enable debug mode

last_track_info = ""
last_track_timestamp = 0
database_path = os.path.join("track_database", "database.txt")

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/now_playing', methods=['GET', 'OPTIONS'])
def now_playing():
    global last_track_info
    global last_track_timestamp
    
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = make_response()
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    asyncio.create_task(handle_track_recording(last_track_info, last_track_timestamp))

    track_data = get_latest_track_info()
    
    logger.info("Hell yeah 2!")
    if track_data:
        title, subtitle = track_data.split(" - ")
        return jsonify({"title": title, "subtitle": subtitle}), 200
    
    return "No recent tracks found.", 204

def get_latest_track_info():
    logger.info("Hell yeah 1!")
    with open(database_path, "r") as file:
        lines = file.readlines()
        if lines:
            latest_track = lines[-1].strip()
            timestamp, title_subtitle = latest_track.split(" | ")
            title, subtitle = title_subtitle.split(" - ")
            
            twelve_seconds_ago = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() - 12))

            if time.mktime(time.strptime(twelve_seconds_ago, "%Y-%m-%d %H:%M:%S")) <= time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")) <= time.mktime(time.strptime(twelve_seconds_ago, "%Y-%m-%d %H:%M:%S")) + 12:
                logger.info("%s - %s", title, subtitle)
                return f"{title} - {subtitle}"
        
        return ""
    
async def loop_track_recording():
    await asyncio.sleep(12)  # Wait for 12 seconds before starting the loop
    while True:
        await handle_track_recording(last_track_info, last_track_timestamp)
        await asyncio.sleep(12)

def track_info_loop():
    while True:
        get_latest_track_info()
        time.sleep(27)

if __name__ == '__main__':
    last_track_timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())  # AKA timestamp
    last_track_info = f"recording_{last_track_timestamp}.wav"  # AKA filename
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_track_recording(last_track_info, last_track_timestamp))  # Run handle_track_recording once initially
    
    loop.create_task(loop_track_recording())   # Start the loop_track_recording task
    
    track_thread = threading.Thread(target=track_info_loop)
    track_thread.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
