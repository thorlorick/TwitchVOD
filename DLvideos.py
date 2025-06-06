from dotenv import load_dotenv
import os
load_dotenv()  # <-- this loads the .env file

import requests
import random
import json
import subprocess
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
USER_ID = os.getenv('USER_ID')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
UPLOADED_LOG = "uploaded_vods.txt"

def get_all_recent_vods():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Client-ID': CLIENT_ID
    }
    url = f'https://api.twitch.tv/helix/videos?user_id={USER_ID}&first=10&type=archive'
    response = requests.get(url, headers=headers).json()
    return response.get("data", [])

def download_vod(vod_id):
    vod_url = f"https://www.twitch.tv/videos/{vod_id}"
    output_filename = f"video_{vod_id}.mp4"
    command = ["streamlink", vod_url, "best", "-o", output_filename]
    subprocess.run(command, check=True)
    return output_filename

def get_random_line(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return random.choice(lines)

def get_random_metadata():
    title = get_random_line("titles.txt")
    description = get_random_line("descriptions.txt")
    tags = [
        "Throne and Liberty", "PGA Tour", "MMO", "MMORPG", "Solisium",
        "El Sarru Kibrat", "Fenikkusu", "Golf Lore", "Live Gaming",
        "Rise from the Ashes", "FelipeManuel", "Pippin Server"
    ]
    random.shuffle(tags)
    return title, description, tags[:10]

def authenticate_youtube():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                "client_secret.json",
                scopes=SCOPES,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob"
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            print("Go to this URL in a browser and authorize the app:\n")
            print(auth_url)
            code = input("\nEnter the authorization code: ")
            flow.fetch_token(code=code)
            creds = flow.credentials

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


def upload_video(youtube, file, title, description, tags):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "20"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(file)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print("Upload successful:", response["id"])

def already_uploaded(vod_id):
    if not os.path.exists(UPLOADED_LOG):
        return False
    with open(UPLOADED_LOG, "r") as f:
        return vod_id in f.read()

def mark_as_uploaded(vod_id):
    with open(UPLOADED_LOG, "a") as f:
        f.write(vod_id + "\n")

def main():
    vods = get_all_recent_vods()
    if not vods:
        print("No VODs found.")
        return

    youtube = authenticate_youtube()

    for vod in vods:
        vod_id = vod["id"]
        vod_title = vod["title"]

        print(f"\nChecking VOD: {vod_title} ({vod_id})")

        if already_uploaded(vod_id):
            print("Already uploaded. Skipping.")
            continue

        video_file = download_vod(vod_id)
        print("Downloaded:", video_file)

        title, description, tags = get_random_metadata()
        print("Uploading with Title:", title)

        upload_video(youtube, video_file, title, description, tags)
        mark_as_uploaded(vod_id)

if __name__ == "__main__":
    main()
