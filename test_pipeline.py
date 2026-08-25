from src.transcript import get_transcript
from src.vectorstore import create_vectorstore

video_id = "dQw4w9WgXcQ"                          # same test video as before

transcript_text = get_transcript(video_id)          # fetch transcript
print("Transcript fetched, length:", len(transcript_text))

vectorstore = create_vectorstore(transcript_text)    # chunk + embed + store
print("Vectorstore created successfully!")

results = vectorstore.similarity_search("what does the song say about giving up", k=2)   # quick similarity test
for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content)