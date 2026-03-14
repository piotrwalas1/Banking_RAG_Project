import os
import shutil
import re
import time
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma

# --- Uwaga!!! KONFIGURACJA Wpisz swoj project id---
PROJECT_ID = "Tu wpisz Twoj project id"
LOCATION = "us-central1"

SOURCE_DIR = r"C:\Users\radek\Desktop\Banking_RAG_Project\documents"
DB_DIR = r"C:\Users\radek\Desktop\Banking_RAG_Project\db"
# --------------------

def clean_text(text):
    
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def create_db_by_pages():
    
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
        print("🗑️ Czyszczenie starej bazy...")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Folder źródłowy nie istnieje: {SOURCE_DIR}")
        return

    all_pages = []
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".pdf")]
    
    if not files:
        print(f"❌ Nie znaleziono plików PDF w {SOURCE_DIR}")
        return

    #  Ładowanie plików strona po stronie
    for file in files:
        print(f"📖 Przetwarzanie dokumentu: {file}")
        file_path = os.path.join(SOURCE_DIR, file)
        loader = PyMuPDFLoader(file_path)
        pages = loader.load()
        
        for i, page in enumerate(pages):
           
            source_info = f"DOKUMENT: {file}, STRONA: {i+1}\n\n"
            page.page_content = source_info + clean_text(page.page_content)
            all_pages.append(page)

    print(f"✂️ Przygotowano {len(all_pages)} stron do wektoryzacji.")

    #  Konfiguracja Vertex AI Embeddings
    print(f"🚀 Inicjalizacja Vertex AI (Project: {PROJECT_ID})...")
    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=LOCATION
    )

    
    batch_size = 5  # Rozsądna wielkość paczki dla stabilności
    delay = 3       # Krótka przerwa między paczkami :)

    try:
        print("🔍 Testowanie połączenia z Google Cloud...")
        
        vector_db = Chroma.from_documents(
            documents=all_pages[:batch_size],
            embedding=embeddings,
            persist_directory=DB_DIR
        )
        print("✅ Pierwsza paczka zapisana.")

       
        for i in range(batch_size, len(all_pages), batch_size):
            batch = all_pages[i:i+batch_size]
            time.sleep(delay)
            vector_db.add_documents(batch)
            print(f"✅ Postęp: {i+len(batch)}/{len(all_pages)}")

        print("\n✨ SUKCES: Nowa baza bankowa została zbudowana!")

    except Exception as e:
        print(f"❌ BŁĄD: {e}")
        print("\nUpewnij się, że w terminalu wpisano: gcloud auth application-default login")

if __name__ == "__main__":
    create_db_by_pages()