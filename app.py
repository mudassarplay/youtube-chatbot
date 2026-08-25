import streamlit as st
from src.transcript import get_transcript
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

if st.button("Load Video"):
    video_id = extract_video_id(video_url)                    # call the function here to get the ID
    with st.spinner("Fetching transcript and building knowledge base..."):
        transcript_text = get_transcript(video_id)
        st.session_state.vectorstore = create_vectorstore(transcript_text)
    st.success("Video loaded! You can ask questions now.")

if st.session_state.vectorstore:
    question = st.text_input("Ask a question about the video")
    if question:
        with st.spinner("Thinking..."):
            answer = get_answer(st.session_state.vectorstore, question)
        st.write("**Answer:**", answer)