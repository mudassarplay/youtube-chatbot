import requests                                          # for fetching video title
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str) -> str:
    """Fetches the transcript of a YouTube video and returns it as one combined string."""
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)
    full_text = " ".join([snippet.text for snippet in fetched_transcript])
    return full_text


def get_video_title(video_id: str) -> str:
    """Fetches the video's title using YouTube's public oEmbed endpoint (no API key needed)."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("title", "Unknown title")
    return "Unknown title"