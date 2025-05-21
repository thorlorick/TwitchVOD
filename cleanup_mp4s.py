import os

directory = "/home/username/twitchvod"

for filename in os.listdir(directory):
    if filename.endswith(".mp4"):
        file_path = os.path.join(directory, filename)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
