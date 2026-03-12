# Banking_RAG_Project - w budowie :)
📂 Struktura Projektu

ingest.py
Wczytuje regulaminy PDF, dzieli je na 1000-znakowe fragmenty i tworzy wektorową bazę danych przy użyciu modelu embeddingów Google.

bank_bot.py
Główny silnik bota, który łączy model Gemini 2.0 Flash z bazą wektorową, umożliwiając inteligentne odpowiadanie na pytania w oparciu o kontekst.

test_runner.py
Skrypt do automatycznej ewaluacji bota, który przesyła pytania z zestawu testowego i ocenia poprawność odpowiedzi za pomocą sędziego AI.

test_cases.json
Plik konfiguracyjny zawierający zestaw 60 pytań testowych wraz z oczekiwanymi odpowiedziami, służący do weryfikacji skuteczności systemu.

documents/
Folder wejściowy przeznaczony na pliki PDF z regulaminami i dokumentacją bankową Santander Bank Polska.

db/
Lokalna baza danych wektorowych ChromaDB, w której przechowywane są przetworzone i zindeksowane fragmenty dokumentów.
