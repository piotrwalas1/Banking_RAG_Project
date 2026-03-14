import os
import time
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# ---Uwaga!!! KONFIGURACJA wpisz swoj project id---
PROJECT_ID = "tu wpisz project id"
LOCATION = "us-central1"
DB_DIR = r"C:\Users\radek\Desktop\Banking_RAG_Project\db"

def get_rag_chain():
    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004",
        project=PROJECT_ID,
        location=LOCATION
    )
    vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    llm = ChatVertexAI(
        model_name="gemini-2.0-flash",
        project=PROJECT_ID,
        location=LOCATION,
        temperature=0,
    )
    system_prompt = (
        "Jesteś ekspertem bankowym Santander. Odpowiadaj konkretnie na podstawie dokumentów.\n\n"
        "KONTEKST:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(vector_db.as_retriever(search_kwargs={"k": 6}), combine_docs_chain)

def invoke_with_metrics(chain, query):
    """Ta funkcja jest niezbędna dla test_runner.py"""
    start_time = time.time()
    response = chain.invoke({"input": query})
    end_time = time.time()
    
    return {
        "answer": response["answer"],
        "latency": round(end_time - start_time, 3),
        "source_count": len(response.get("context", []))
    }

def run_bank_bot():
    rag_chain = get_rag_chain()
    print("✅ Bot Santander gotowy!")
    while True:
        query = input("\n👤 Klient: ")
        if query.lower() in ['exit', 'koniec']: break
        res = invoke_with_metrics(rag_chain, query)
        print(f"🤖 Bot: {res['answer']}")
        print(f"\n[⏱️ Latency: {res['latency']}s | 📄 Źródła: {res['source_count']} chunks]")

if __name__ == "__main__":
    run_bank_bot()