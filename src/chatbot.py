from langchain_ollama import ChatOllama

def get_answer(vectorstore, question: str, video_title: str = "") -> str:      # added video_title parameter
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    llm = ChatOllama(model="qwen2.5:3b-instruct", temperature=0.3)

    prompt = f"""You are a helpful assistant answering questions about a YouTube video, based on its title and transcript.

Video Title: {video_title}

Answer clearly and in a complete, natural sentence.
If the answer isn't in the title or context, say so politely and briefly explain what you do know instead.

Context from the video transcript:
{context}

Question: {question}

Answer in a friendly, conversational tone:"""

    response = llm.invoke(prompt)
    return response.content