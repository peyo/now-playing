from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import asyncio
import threading
import time
import os
from api.modules.track_record import handle_track_recording

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

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
    
@app.route('/api/check_new_entry', methods=['GET'])
def check_new_entry():
    # Construct the path to the database file
    database_file = os.path.join(current_dir, 'track_database', 'database.txt')

    # Read the contents of the database file
    with open(database_file, 'r') as file:
        lines = file.readlines()
    
    # Extract the timestamp of the last entry in the database
    last_entry = lines[-1].strip().split('|')
    last_timestamp = last_entry[0].strip() if last_entry else None
    
    # Get the current timestamp
    current_timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    
    if last_timestamp:
        last_entry_time = time.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")
        current_time = time.strptime(current_timestamp, "%Y%m%d-%H%M%S")
        time_difference = time.mktime(current_time) - time.mktime(last_entry_time)
        
        if time_difference <= 27:
            # New entry detected, send the new entry to the frontend
            return jsonify({'new_entry': last_entry}), 200
    
    # No new entry detected
    return jsonify({'new_entry': None}), 200

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