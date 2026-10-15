"""Shared YouTube login and helpers."""
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(HERE, "client_secret.json")
TOKEN = os.path.join(HERE, "token.json")
# force-ssl covers reading comments and posting replies, so one login is enough for every step.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_service():
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
        creds = flow.run_local_server(port=0, prompt="consent")
    with open(TOKEN, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN, 0o600)
    return build("youtube", "v3", credentials=creds)


def my_channel(yt):
    ch = yt.channels().list(part="snippet,contentDetails", mine=True).execute()["items"][0]
    return ch


def comment_threads(yt, video_id):
    """Yield every top-level comment thread on a video, with all its replies."""
    token = None
    while True:
        resp = yt.commentThreads().list(
            part="snippet,replies", videoId=video_id, maxResults=100,
            pageToken=token, textFormat="plainText").execute()
        for t in resp.get("items", []):
            n = t["snippet"]["totalReplyCount"]
            replies = t.get("replies", {}).get("comments", [])
            if n > len(replies):
                replies = yt.comments().list(
                    part="snippet", parentId=t["id"], maxResults=100,
                    textFormat="plainText").execute().get("items", [])
            t["all_replies"] = replies
            yield t
        token = resp.get("nextPageToken")
        if not token:
            return


def author_id(c):
    return c["snippet"].get("authorChannelId", {}).get("value")
