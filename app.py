import streamlit as st
from src.transcript import get_transcript, get_video_title
from src.vectorstore import create_vectorstore
from src.chatbot import get_answer


def extract_video_id(url: str) -> str:
    """Extracts the YouTube video ID from either youtube.com or youtu.be style URLs."""
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    elif "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0]
    else:
        video_id = url
    return video_id


st.title("🎥 YouTube Chatbot")
st.write("Paste a YouTube video link and ask questions about it.")

video_url = st.text_input("YouTube Video URL")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "video_title" not in st.session_state:
    st.session_state.video_title = ""

if "chat_history" not in st.session_state:                 # NEW: list to store (question, answer) pairs
    st.session_state.chat_history = []

if st.button("Load Video"):
    video_id = extract_video_id(video_url)
    with st.spinner("Fetching transcript and building knowledge base..."):
        transcript_text = get_transcript(video_id)
        st.session_state.vectorstore = create_vectorstore(transcript_text)
        st.session_state.video_title = get_video_title(video_id)
        st.session_state.chat_history = []                    # NEW: reset chat when a new video loads
    st.success(f"Loaded: {st.session_state.video_title}")

if st.session_state.vectorstore:
    for question, answer in st.session_state.chat_history:     # NEW: redraw all previous messages
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)

    question = st.chat_input("Ask a question about the video")  # NEW: chat-style input box

    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = get_answer(st.session_state.vectorstore, question, st.session_state.video_title)
            st.write(answer)

        st.session_state.chat_history.append((question, answer))   # NEW: save this exchange