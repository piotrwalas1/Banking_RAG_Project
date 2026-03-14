# Banking_RAG_Project - w budowie :)
# 🏦 BankBot RAG: System Automatycznej Obsługi Klienta Bankowego

## 📖 Opis Projektu
Projekt to zaawansowany system typu **RAG (Retrieval-Augmented Generation)**, zaprojektowany do precyzyjnego udzielania odpowiedzi na pytania dotyczące oferty bankowej (opłaty, prowizje, regulaminy). System wykorzystuje wyszukiwanie semantyczne (Vector Search) oraz modele językowe klasy Enterprise, aby dostarczać rzetelne informacje w oparciu o autentyczne dokumenty Santander Bank Polska.



## 🏗️ Architektura Skryptów

Projekt składa się z trzech modułów, które automatyzują pełny cykl życia systemu AI:

### 1. `ingest.py` (Procesowanie Danych)
* **Zadanie:** Ekstrakcja wiedzy z dokumentów PDF i budowa bazy wektorowej.
* **Technologia:** Wykorzystuje **LangChain** do dzielenia tekstu (chunking) oraz model **text-embedding-004** (Google) do tworzenia reprezentacji wektorowych.
* **Wynik:** Lokalna baza **ChromaDB**, umożliwiająca wyszukiwanie kontekstowe zamiast prostego dopasowania słów kluczowych.

### 2. `bank_bot.py` (Silnik Konwersacyjny)
* **Zadanie:** Główny mózg bota łączący bazę wiedzy z modelem **Gemini 2.0 Flash**.
* **Logika:** Implementuje łańcuch RAG, który pobiera relewantne fragmenty dokumentów i wstrzykuje je do bezpiecznego promptu systemowego.
* **Monitoring:** Posiada wbudowaną funkcję `invoke_with_metrics`, mierzącą opóźnienie (latency) oraz liczbę pobranych źródeł (chunks) dla każdego zapytania.

### 3. `test_runner.py` (Moduł Audytu i Ewaluacji)
* **Zadanie:** Zautomatyzowany benchmark jakości i wydajności.
* **Metodologia LLM-as-a-Judge:** Wykorzystuje model **Gemini 2.5 Pro** jako niezależnego audytora, który ocenia merytoryczną poprawność odpowiedzi bota w skali 1-5 na podstawie bazy 60 rzeczywistych przypadków testowych.

---

## 📏 Metodologia Pomiarowa (Kluczowe Metryki)

System jest monitorowany w trzech kluczowych wymiarach:

1.  **Merytoryka (Accuracy):**
    * **Context Hit Rate:** Czy silnik odnalazł właściwy fragment dokumentu?
    * **Answer Correctness:** Porównanie odpowiedzi bota z wzorcem przy użyciu zaawansowanego modelu oceniającego.
2.  **Wydajność (Performance):**
    * **Latency (Opóźnienie):** Czas odpowiedzi (kluczowy dla standardów UX w sektorze finansowym).
3.  **Ekonomia (Cloud FinOps):**
    * **Cost per Query:** Precyzyjne wyliczenie kosztu zapytania na podstawie zużycia tokenów (input/output).

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
* **Wnioski:** System niemal bezbłędnie (ponad 98%) odnajduje właściwe dokumenty w bazie.
* **Knowledge Gaps:** Audyt wykazał brak danych dla produktu "Konto Jakie Chcę" (brak pliku źródłowego). System zachował się poprawnie – zamiast halucynować, poinformował o braku informacji, co jest krytyczne dla bezpieczeństwa bankowego.

#### 2. Filar Generation (Jakość AI)
* **Analiza:** Najwyższe noty (5/5) bot uzyskuje przy zapytaniach o konkretne kwoty i proste procedury.
* **Obszary do poprawy:** Niższe oceny (1/5) pojawiają się przy zapytaniach wymagających syntezy wiedzy z wielu stron regulaminu jednocześnie (np. złożone kwestie spadkowe). Rekomendowane jest zwiększenie okna kontekstowego dla tych zagadnień.

#### 3. Filar Performance & Business
* **UX:** Średnie opóźnienie **1.35s** pozwala na płynną, naturalną interakcję z klientem bez "efektu czekania".
* **Skalowalność:** Koszt jednostkowy zapytania (**$0.0027**) udowadnia, że model Gemini 2.0 Flash zapewnia bezkonkurencyjny stosunek jakości do ceny w zastosowaniach masowych.

---
*Projekt zrealizowany w ramach benchmarkingu i optymalizacji systemów RAG dla sektora bankowego.*
