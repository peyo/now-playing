from flask import Flask, jsonify, request
import asyncio
import threading
import time
from api.modules.track_record import handle_track_recording

app = Flask(__name__)

recording_active = False  # Flag to indicate if recording is active
loop_interval = 12  # Interval between recording loops in seconds

@app.route('/api/start', methods=['POST'])
def record_endpoint():
    global recording_active

    if request.method == 'POST':
        if not recording_active:
            recording_active = True
            return 'Recording activated.'
        else:
            return 'Recording already active.'
    else:
        return 'Invalid request method.'

@app.route('/api/stop', methods=['POST'])
def stop_endpoint():
    global recording_active

    if request.method == 'POST':
        if recording_active:
            recording_active = False
            return 'Recording stopped.'
        else:
            return 'No active recording.'
    else:
        return 'Invalid request method.'

def track_recording_loop():
    global recording_active

    while True:
        if recording_active:
            timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
            filename = f"recording_{timestamp}.wav"
            asyncio.run(handle_track_recording(filename, timestamp))

        time.sleep(loop_interval)

if __name__ == '__main__':
    track_thread = threading.Thread(target=track_recording_loop)
    track_thread.start()

    app.run()