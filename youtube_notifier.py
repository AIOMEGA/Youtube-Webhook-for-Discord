import requests
import os

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = "UC7WYnIkI2Dz9ynsHm4IvwVg"
UPLOADS_PLAYLIST_ID = "UU7WYnIkI2Dz9ynsHm4IvwVg"
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
GIST_ID = os.environ.get("GIST_ID")
GITHUB_TOKEN = os.environ.get("GIST_TOKEN")

GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"
YOUTUBE_PLAYLIST_ITEMS_URL = (
    f"https://www.googleapis.com/youtube/v3/playlistItems"
    f"?part=snippet&maxResults=5&playlistId={UPLOADS_PLAYLIST_ID}&key={YOUTUBE_API_KEY}"
)
YOUTUBE_VIDEO_DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos"

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

def notify_discord(title, url, video_type="Video"):
    emoji = {
        "Video": "📢",
        "Short": "🎬",
        "Live": "🔴"
    }.get(video_type, "📢")

    data = {
        "content": f"<@&1357010336791793805>\n{emoji} New **{video_type}** uploaded!\n**{title}**\n{url}"
    }
    requests.post(WEBHOOK_URL, json=data)

def get_video_type(video_id):
    params = {
        "part": "snippet,liveStreamingDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }
    res = requests.get(YOUTUBE_VIDEO_DETAILS_URL, params=params)
    if res.status_code == 200:
        items = res.json().get("items", [])
        if not items:
            return "Video"

        video = items[0]
        snippet = video.get("snippet", {})
        live_details = video.get("liveStreamingDetails", {})

        # Detect livestream
        if live_details:
            return "Live"

        # Detect shorts by video URL format
        # Technically this could be guessed by duration, but better to use format
        if snippet.get("categoryId") == "22" and "/shorts/" in snippet.get("description", ""):
            return "Short"

    return "Video"

def get_recent_videos():
    res = requests.get(YOUTUBE_PLAYLIST_ITEMS_URL)
    videos = []
    if res.status_code == 200:
        items = res.json().get("items", [])
        for item in items:
            snippet = item["snippet"]
            video_id = snippet["resourceId"]["videoId"]
            title = snippet["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                "id": video_id,
                "title": title,
                "url": url
            })
    return videos

def main():
    last_id = get_last_video_id()
    recent_videos = get_recent_videos()

    if not recent_videos:
        return

    new_videos = []
    for video in recent_videos:
        if video["id"] == last_id:
            break
        new_videos.append(video)

    if new_videos:
        for video in reversed(new_videos):  # Oldest first
            video_type = get_video_type(video["id"])
            notify_discord(video["title"], video["url"], video_type)
        save_last_video_id(recent_videos[0]["id"])

if __name__ == "__main__":
    main()
