from youtube_transcript_api import YouTubeTranscriptApi   # library to fetch YouTube transcripts

def get_transcript(video_id: str) -> str:
    """Fetches the transcript of a YouTube video and returns it as one combined string."""
    ytt_api = YouTubeTranscriptApi()                          # create an instance (new API style)
    fetched_transcript = ytt_api.fetch(video_id)               # fetch the transcript for this video ID
    full_text = " ".join([snippet.text for snippet in fetched_transcript])  # join all text pieces into one string
    return full_text


