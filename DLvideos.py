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
