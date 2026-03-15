# 🏦 BankBot RAG: System Automatycznej Obsługi Klienta Bankowego

## 📖 Opis Projektu
Projekt to zaawansowany system typu **RAG (Retrieval-Augmented Generation)**, zaprojektowany do precyzyjnego udzielania odpowiedzi na pytania dotyczące oferty bankowej (opłaty, prowizje, regulaminy). System łączy potęgę wyszukiwania semantycznego (Vector Search) z zaawansowanym wnioskowaniem modeli językowych klasy Enterprise, co pozwala na automatyzację obsługi klienta przy zachowaniu najwyższej wiarygodności danych.



## 🏗️ Architektura Skryptów

Projekt składa się z trzech modułów, które automatyzują pełny cykl życia systemu AI:

### 1. `ingest.py` (Procesowanie Danych)
* **Zadanie:** Ekstrakcja wiedzy z surowych dokumentów PDF (TOiP, regulaminy) i budowa bazy wiedzy.
* **Technologia:** Wykorzystuje **LangChain** do zaawansowanego dzielenia tekstu (chunking) oraz model **text-embedding-004** (Google) do tworzenia wektorowych reprezentacji znaczenia.
* **Wynik:** Lokalna baza wektorowa **ChromaDB**, umożliwiająca błyskawiczne przeszukiwanie dokumentów na podstawie kontekstu, a nie tylko słów kluczowych.

### 2. `bank_bot.py` (Silnik Konwersacyjny)
* **Zadanie:** Główny silnik bota łączący bazę wiedzy z modelem **Gemini 2.0 Flash**.
* **Logika:** Implementuje łańcuch RAG, który dla każdego zapytania pobiera najbardziej relewantne fragmenty dokumentów i wstrzykuje je do bezpiecznego promptu systemowego.
* **Monitoring:** Zawiera funkcję `invoke_with_metrics`, która w czasie rzeczywistym monitoruje opóźnienie (latency) oraz liczbę pobranych źródeł (chunks).

### 3. `test_runner.py` (Moduł Audytu i Zaawansowanej Ewaluacji)
* **Zadanie:** Kompleksowy, zautomatyzowany benchmark jakościowy (Quality Assurance) oraz wydajnościowy całego potoku RAG.
* **Metodologia LLM-as-a-Judge:** W projekcie zaimplementowano podejście, w którym model wyższej klasy (**Gemini 2.5 Pro**) pełni rolę niezależnego audytora. Sędzia analizuje odpowiedzi modelu bazowego i porównuje je ze "złotym zbiorem" (Golden Dataset) 60 rzeczywistych przypadków testowych.
* **Mierzone metryki:**
    * **Answer Correctness (Merytoryka):** Zgodność odpowiedzi z faktami w dokumentach.
    * **Faithfulness / Groundedness (Wierność):** Weryfikacja, czy bot nie generuje halucynacji.
    * **Retrieval Hit Rate:** Skuteczność odnajdywania właściwych dokumentów.
    * **Performance & FinOps:** Monitorowanie czasu odpowiedzi (Latency) oraz kosztu jednostkowego zapytania (Cost per Query).
    * 
### 4. `dashboard.py` (Analytical Dashboard)
* **Technologia:** **Streamlit & Plotly**.
* **Zadanie:** Wizualizacja wyników testów, analiza rozkładu ocen oraz monitoring wydajności (FinOps).

---

## 📊 Raport Ewaluacyjny (Stan na 2026-03-14)

### Podsumowanie Zbiorcze (Executive Summary)

| Metryka | Wynik | Interpretacja |
| :--- | :--- | :--- |
| **Skuteczność Wyszukiwania (Hit Rate)** | **98.33%** | 🟢 Celująca |
| **Średni Wynik Merytoryczny** | **3.67 / 5.0** | 🟡 Dobra |
| **Średnie Opóźnienie (Latency)** | **1.351 s** | 🟢 Celująca |
| **Koszt Audytu (60 pytań)** | **0.16 USD** | 🟢 Optymalna |



### Szczegółowa Analiza Filarów RAG

#### 1. Filar Retrieval (Wyszukiwanie)
* **Wnioski:** System niemal bezbłędnie (ponad 98%) odnajduje właściwe dokumenty w bazie wektorowej.
* **Knowledge Gaps:** Audyt wykazał brak danych dla produktu "Konto Jakie Chcę" (brak pliku źródłowego). System zachował się poprawnie – zamiast halucynować, poinformował o braku informacji, co jest krytyczne dla bezpieczeństwa bankowego.

#### 2. Filar Generation (Jakość AI)
* **Analiza:** Najwyższe noty (5/5) bot uzyskuje przy zapytaniach o konkretne kwoty i proste procedury.
* **Obszary do poprawy:** Niższe oceny (1/5) pojawiają się przy zapytaniach wymagających syntezy wiedzy z wielu stron regulaminu jednocześnie (np. złożone kwestie spadkowe). Rekomendowane jest zwiększenie okna kontekstowego dla tych zagadnień.

#### 3. Filar Performance & Business
* **UX:** Średnie opóźnienie **1.35s** pozwala na natychmiastową interakcję z klientem bez "efektu czekania".
* **Skalowalność:** Koszt jednostkowy zapytania (**$0.0027**) udowadnia, że model Gemini 2.0 Flash zapewnia najlepszy stosunek jakości do ceny w zastosowaniach Enterprise.
