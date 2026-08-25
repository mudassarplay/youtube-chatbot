from src.transcript import get_transcript
from src.vectorstore import create_vectorstore
from src.chatbot import get_answer

video_id = "dQw4w9WgXcQ"

transcript_text = get_transcript(video_id)
print("Transcript fetched, length:", len(transcript_text))

vectorstore = create_vectorstore(transcript_text)
print("Vectorstore created successfully!")

question = "What does the singer promise to never do?"
answer = get_answer(vectorstore, question)
print("\nQuestion:", question)
print("Answer:", answer)