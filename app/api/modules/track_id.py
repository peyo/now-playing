# Use the shazamio package to identify the latest record file found in ./app/recordings.

from shazamio import Shazam     # Shazamio functionality
import os                       # File identification/paths
import time                     # Time (logging & timestamps for files)

async def identify_track(output_folder):
  shazam = Shazam()
  latest_file = get_latest_file(output_folder)
  if latest_file:
        try:
            out = await shazam.recognize_song(latest_file)
            title = out['track']['title']
            subtitle = out['track']['subtitle']
            print("track_id.py:", subtitle, "-", title)
            save_track_data(subtitle, title)  # Save the data to the text file
            return subtitle, title
        except KeyError:
            print("track_id.py:", "No recent track information found.")
            save_track_data("Song not found.", None)  # Save the data to the text file
            return None, None
  else:
        print("track_id.py:", "No files found in the output folder.")
        save_track_data("Song not found.", None)  # Save the data to the text file
        return None, None

def get_latest_file(output_folder):
    files = os.listdir(output_folder)
    if not files:
        return None

    files = [os.path.join(output_folder, f) for f in files]
    latest_file = max(files, key=os.path.getctime)
    return latest_file

# Save track information to track_database.database.txt
def save_track_data(subtitle, title):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(current_dir, '..', '..', 'track_database')
    os.makedirs(database_dir, exist_ok=True)  # Create the 'track_database' directory if it doesn't exist

    database_file = os.path.join(database_dir, 'database.txt')

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    data = f"{timestamp} | {subtitle} - {title}\n"

    with open(database_file, 'a') as file:
        file.write(data)