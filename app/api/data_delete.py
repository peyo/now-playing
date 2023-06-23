import os

def delete_oldest_line(database_file, max_lines):
    database_path = os.path.join(os.path.dirname(__file__), database_file)

    with open(database_file, "r") as file:
        lines = file.readlines()

    if len(lines) > max_lines:
        lines = lines[1:]  # Remove the oldest line (first line)

        with open(database_file, "w") as file:
            file.writelines(lines)

        print("data_delete.py:", "Deleted oldest line from the database.")

if __name__ == "__main__":
    database_file = "../track_database/database.txt"
    max_lines = 100
    delete_oldest_line(database_file, max_lines)