from fastapi import FastAPI                              # the framework itself
from pydantic import BaseModel                             # for defining request data shapes
from src.transcript import get_transcript, get_video_title
from src.vectorstore import create_vectorstore
from src.chatbot import get_answer
from fastapi.middleware.cors import CORSMiddleware   # NEW: import CORS support

app = FastAPI()                                             # create the FastAPI application
# NEW: allow requests from any origin (fine for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # "*" means allow any website/address to call this API
    allow_credentials=True,
    allow_methods=["*"],          # allow all request types (GET, POST, etc.)
    allow_headers=["*"],
)

# In-memory storage for the current session (simple, single-user, good enough for learning)
session = {
    "vectorstore": None,
    "video_title": ""
}


def extract_video_id(url: str) -> str:
    """Extracts the YouTube video ID from either youtube.com or youtu.be style URLs."""
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    elif "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0]
    else:
        video_id = url
    return video_id


class LoadVideoRequest(BaseModel):                          # defines what data /load-video expects
    url: str


class AskRequest(BaseModel):                                # defines what data /ask expects
    question: str


@app.post("/load-video")
def load_video(request: LoadVideoRequest):
    video_id = extract_video_id(request.url)
    transcript_text = get_transcript(video_id)
    session["vectorstore"] = create_vectorstore(transcript_text)
    session["video_title"] = get_video_title(video_id)
    return {"title": session["video_title"]}


@app.post("/ask")
def ask(request: AskRequest):
    answer = get_answer(session["vectorstore"], request.question, session["video_title"])
    return {"answer": answer}