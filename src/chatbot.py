from langchain_ollama import ChatOllama              # your local model wrapper

def get_answer(vectorstore, question: str) -> str:
    """Takes a vectorstore and a question, retrieves relevant chunks, and asks the LLM to answer using them."""

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})   # get top 3 relevant chunks
    relevant_docs = retriever.invoke(question)                      # actually fetch them

    context = "\n\n".join([doc.page_content for doc in relevant_docs])   # combine all chunks into one context block

    llm = ChatOllama(model="qwen2.5:3b-instruct")                   # your local model

    prompt = f"""Answer the question based only on the following context from a video transcript.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}

Answer:"""

    response = llm.invoke(prompt)          # send the prompt to the LLM
    return response.content                 # return just the text answer