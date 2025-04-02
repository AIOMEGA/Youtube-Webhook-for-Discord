import requests
import os

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = "UC7WYnIkI2Dz9ynsHm4IvwVg"
UPLOADS_PLAYLIST_ID = "UU7WYnIkI2Dz9ynsHm4IvwVg"
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
GIST_ID = os.environ.get("GIST_ID")
GITHUB_TOKEN = os.environ.get("GIST_TOKEN")

GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"
YOUTUBE_API_URL = (
    f"https://www.googleapis.com/youtube/v3/playlistItems"
    f"?part=snippet&maxResults=1&playlistId={UPLOADS_PLAYLIST_ID}&key={YOUTUBE_API_KEY}"
)

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_last_video_id():
    res = requests.get(GIST_API_URL, headers=HEADERS)
    if res.status_code == 200:
        files = res.json().get("files", {})
        content = files.get("last_video_id.txt", {}).get("content", "").strip()
        return content if content else None
    return None

def save_last_video_id(video_id):
    data = {
        "files": {
            "last_video_id.txt": {
                "content": video_id
            }
        }
    }
    requests.patch(GIST_API_URL, headers=HEADERS, json=data)

# Has the webhook send a messge informing of an upload and @'ing a server role.
def notify_discord(title, url):
    data = {
        "content": f"<@&1357010336791793805>\n📢 New video uploaded!\n**{title}**\n{url}"
    }
    requests.post(WEBHOOK_URL, json=data)

def get_latest_video():
    res = requests.get(YOUTUBE_API_URL)
    if res.status_code == 200:
        items = res.json().get("items", [])
        if items:
            video_id = items[0]["snippet"]["resourceId"]["videoId"]
            title = items[0]["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            return video_id, title, url
    return None, None, None

def main():
    latest_id, title, url = get_latest_video()
    if not latest_id:
        return

    last_id = get_last_video_id()
    if latest_id != last_id:
        notify_discord(title, url)
        save_last_video_id(latest_id)

if __name__ == "__main__":
    main()