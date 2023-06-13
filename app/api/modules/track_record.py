# Record tracks and send them to track_id to identify and run track_delete to maintain the folder to five tracks

import os                                   # File identification/paths
import time                                 # Time (logging & timestamps for files)
from shazamio import Shazam                 # Shazamio functionality
import asyncio                              # Write asynchronous code
import pyaudio                              # Recording functionality
import wave                                 # Recording functionality
import sys                                  # Access system-specific parameters and functions

# Add the current directory to the Python module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from track_delete import delete_oldest_file
from track_id import identify_track
from data_delete import delete_oldest_line  

# Configuration from recording
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1                                # Set the number of audio channels to 1 for mono
sample_rate = 44100
record_duration = 12                        # Duration of each audio snippet in seconds
extension = ".wav"

current_dir = os.path.dirname(os.path.abspath(__file__))                                    # Get the directory of the current Python script
output_folder = os.path.join(current_dir, "..", "..", "recordings")                         # Construct the path to the desired folder
database_file = os.path.join(current_dir, "..", "..", "track_database", "database.txt")     # Define the database file path

track_record_success = False    # Global variable to track the status of track recording

def record_track():
    p = pyaudio.PyAudio()

    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=sample_rate,
        frames_per_buffer=chunk,
        input=True
    )

    frames = []

    print("track_record.py", "Recording...")

    for i in range(0, int(sample_rate / chunk * record_duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("track_record.py", "Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames

def save_audio(frames, filename):    
    p = pyaudio.PyAudio()

    output_path = os.path.join(output_folder, filename)
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

async def handle_track_recording(filename, timestamp):  # main
    if filename != "":
        frames = record_track()
        save_audio(frames, filename)
        print("track_record.py", "Saved recording:", filename)

        new_recording_available = True

        max_files = 5
        delete_oldest_file(output_folder, max_files)

        max_lines = 100
        delete_oldest_line(database_file, max_lines)

        if new_recording_available:
            await identify_track(output_folder)
            new_recording_available = False

if __name__ == "__main__":
    timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    filename = f"recording_{timestamp}.wav"
    asyncio.run(handle_track_recording(filename, timestamp))