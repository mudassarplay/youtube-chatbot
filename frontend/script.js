const API_URL = "http://127.0.0.1:8000";        // same backend URL as before

let currentVideoTitle = "";                        // tracks which video is currently loaded

// --- Show/hide chat vs welcome screen ---
function showChatView() {
    document.getElementById("welcome-screen").style.display = "none";
    document.getElementById("chat-input-area").style.display = "flex";
    document.getElementById("close-chat-btn").style.display = "inline-block";
}

function showWelcomeView() {
    document.getElementById("welcome-screen").style.display = "flex";
    document.getElementById("chat-input-area").style.display = "none";
    document.getElementById("close-chat-btn").style.display = "none";
    document.getElementById("current-video-title").innerText = "";
    document.getElementById("chat-messages").innerHTML = "";
    currentVideoTitle = "";
}

document.getElementById("close-chat-btn").addEventListener("click", showWelcomeView);

// --- Shared function to load a video (used by sidebar, welcome screen, and past conversations) ---
async function loadVideo(url) {
    const response = await fetch(`${API_URL}/load-video`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    });

    const data = await response.json();
    currentVideoTitle = data.title;

    document.getElementById("current-video-title").innerText = currentVideoTitle;
    document.getElementById("chat-messages").innerHTML = "";

    showChatView();
    loadSidebarHistory();
}

// --- Sidebar "Load Video" button ---
document.getElementById("load-video-btn").addEventListener("click", async () => {
    const url = document.getElementById("video-url").value;
    await loadVideo(url);
});

// --- Welcome screen "Load Video" button ---
document.getElementById("welcome-load-btn").addEventListener("click", async () => {
    const url = document.getElementById("welcome-video-url").value;
    await loadVideo(url);
});

// --- Ask a question ---
document.getElementById("ask-btn").addEventListener("click", async () => {
    const question = document.getElementById("question-input").value;
    if (!question) return;

    addMessage("user", question);
    document.getElementById("question-input").value = "";

    const thinkingBubble = addMessage("assistant", "Thinking...");

    const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question })
    });

    const data = await response.json();
    thinkingBubble.innerText = data.answer;
});

// --- Send message on Enter key ---
document.getElementById("question-input").addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("ask-btn").click();
    }
});

// --- Helper: add a chat bubble to the screen ---
function addMessage(role, text) {
    const messagesDiv = document.getElementById("chat-messages");
    const bubble = document.createElement("div");
    bubble.className = `message ${role}`;
    bubble.innerText = text;
    messagesDiv.appendChild(bubble);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return bubble;
}

// --- Load sidebar list of past videos ---
async function loadSidebarHistory() {
    const response = await fetch(`${API_URL}/history`);
    const allHistory = await response.json();

    const uniqueTitles = [...new Set(allHistory.map(h => h.video_title))];

    const listDiv = document.getElementById("video-list");
    listDiv.innerHTML = "";

    uniqueTitles.forEach(title => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.innerText = title;
        btn.addEventListener("click", () => loadPastConversation(title, allHistory));
        listDiv.appendChild(btn);
    });
}

// --- Load a specific past conversation when clicked in sidebar ---
async function loadPastConversation(title, allHistory) {
    const videoMessages = allHistory.filter(h => h.video_title === title);
    const videoId = videoMessages[0].video_id;                          // get the video's ID from saved history
    const url = `https://www.youtube.com/watch?v=${videoId}`;           // reconstruct a valid URL from it

    await loadVideo(url);                                                 // actually rebuild the vectorstore on the backend

    videoMessages.forEach(h => {
        addMessage("user", h.question);
        addMessage("assistant", h.answer);
    });
}

// --- On page load, show sidebar history right away ---
loadSidebarHistory();