# Maintain the recording folder of up to five files. Delete the oldest file, the sixth file.

import os  # Interact with the operating system

def delete_oldest_file(output_folder, max_files):
    files = os.listdir(output_folder)
    if len(files) <= max_files:
        return

    files = [os.path.join(output_folder, f) for f in files]
    files.sort(key=os.path.getctime)

    oldest_file = files[0]
    os.remove(oldest_file)
    print("track_delete.py:", f"Deleted oldest file: {oldest_file}")