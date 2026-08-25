from langchain_ollama import ChatOllama

def get_answer(vectorstore, question: str, video_title: str = "") -> str:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    llm = ChatOllama(model="qwen2.5:3b-instruct", temperature=0.3)

    prompt = f"""You are a friendly assistant helping a user explore a YouTube video titled "{video_title}".

Guidelines:
- If the user greets you or makes small talk (like "hi", "thanks", "how are you"), respond naturally and warmly — don't mention the transcript for these.
- If the user asks a real question about the video's content, answer using ONLY the transcript context below.
- If the question is about the video but the answer isn't in the context, say honestly that the transcript doesn't cover that.
- If the question is completely unrelated to the video (like asking about the weather, or something random), politely say you can only help with questions about this video.

Transcript context:
{context}

User: {question}

Assistant:"""

    response = llm.invoke(prompt)
    return response.content