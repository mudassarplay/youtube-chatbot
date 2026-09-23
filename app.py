import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🎥 YouTube Chatbot")

if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "video_title" not in st.session_state:
    st.session_state.video_title = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def load_chat_for_video(title):
    """Fetches saved history for a given video title and loads it into the current session."""
    history_response = requests.get(f"{API_URL}/history")
    all_history = history_response.json()
    video_history = [h for h in all_history if h["video_title"] == title]
    st.session_state.chat_history = [(h["question"], h["answer"]) for h in video_history]
    st.session_state.video_title = title
    st.session_state.video_loaded = True


# --- SIDEBAR: past conversations ---
with st.sidebar:
    st.header("💬 Past Conversations")
    history_response = requests.get(f"{API_URL}/history")
    all_history = history_response.json()
    past_titles = sorted(set(h["video_title"] for h in all_history))   # unique video titles

    for title in past_titles:
        if st.button(title, key=f"sidebar_{title}"):
            load_chat_for_video(title)

    st.divider()
    st.header("➕ New Video")
    video_url = st.text_input("YouTube Video URL")
    if st.button("Load Video"):
        with st.spinner("Fetching transcript and building knowledge base..."):
            response = requests.post(f"{API_URL}/load-video", json={"url": video_url})
            data = response.json()
            load_chat_for_video(data["title"])
        st.success(f"Loaded: {st.session_state.video_title}")


# --- MAIN AREA: active chat ---
if st.session_state.video_loaded:
    st.subheader(st.session_state.video_title)

    for question, answer in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)

    question = st.chat_input("Ask a question about the video")

    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(f"{API_URL}/ask", json={"question": question})
                answer = response.json()["answer"]
            st.write(answer)
        st.session_state.chat_history.append((question, answer))
else:
    st.write("👈 Load a video from the sidebar to get started.")