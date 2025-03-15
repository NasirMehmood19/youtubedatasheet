import gspread
import datetime
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Load credentials from the JSON file
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Google Sheet ID
SPREADSHEET_ID = "1rC2bZYsGXLOACAdI0gm9h45T9oUo7rwWbvP68zYz5DA"

# YouTube API Key (Store in GitHub Secrets)
API_KEY = "AIzaSyAQx_XjqsrBQBpfWNExzj6uvmr4t2Uphks"

# YouTube Channels
channels = {
    "UC62pPLZqx8JIrtW1kT5NPWA": "Geo Entertainment",
    "UC_vt34wimdCzdkrzVejwX9g": "Geo News",
}

# Authenticate with Google Sheets
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Fetch YouTube Stats
def get_youtube_client():
    return build("youtube", "v3", developerKey=API_KEY)

def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(part="statistics", id=channel_id)
    response = request.execute()
    if "items" in response and response["items"]:
        stats = response["items"][0]["statistics"]
        return int(stats.get("viewCount", 0)), int(stats.get("subscriberCount", 0))
    return None, None

def fetch_youtube_stats():
    youtube = get_youtube_client()
    today = datetime.date.today().strftime("%Y-%m-%d")
    data = []

    for channel_id, channel_name in channels.items():
        views, subscribers = get_channel_stats(youtube, channel_id)
        if views is not None:
            data.append([today, channel_name, views, subscribers])

    # Append data to Google Sheet
    sheet.append_rows(data, value_input_option="USER_ENTERED")
    print("Data added to Google Sheet successfully.")

if __name__ == "__main__":
    fetch_youtube_stats()
