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

  ## 📊 Wizualizacja Wyników (Dashboard Analityczny)

System posiada zintegrowany interfejs analityczny zbudowany w **Streamlit**, który pozwala na interpretację danych z audytu w czasie rzeczywistym.

 <p align="center">
  <img src="https://github.com/piotrwalas1/Banking_RAG_Project/blob/main/dashboard_preview.png" width="600" title="raport1">
</p>

### Kluczowe elementy raportu:

* **KPI Overview:** Szybki podgląd na najważniejsze wskaźniki:
    * **Średnia Ocena (3.67/5):** Wynik merytoryczny wygenerowany przez model Gemini 2.5 Pro.
    * **Hit Rate (98.33%):** Dowód na niemal idealną skuteczność silnika wyszukiwania wektorowego.
    * **Total Cost ($0.16):** Sumaryczny koszt przeprowadzenia pełnego audytu (60 pytań), co podkreśla ekonomiczność rozwiązania.
* **Score Distribution:** Wykres słupkowy pokazujący rozkład jakości odpowiedzi. Pozwala na szybką identyfikację pytań, przy których model uzyskał niższe noty (np. oceny 1 i 3), co ułatwia debugowanie bazy wiedzy.
* **Latency vs Cost Scatter Plot:** Zaawansowana wizualizacja korelacji między czasem odpowiedzi a kosztem tokenów. Pomaga zlokalizować "ciężkie" zapytania, które wymagają optymalizacji promptu lub chunkingu.
* **Interactive Data Table:** Pełna, filtrowana lista scenariuszy testowych. Umożliwia szczegółową analizę konkretnych odpowiedzi bota wraz z uzasadnieniem sędziego AI oraz bezpośredni eksport danych do pliku CSV.

---

## 📥 Pobieranie danych testowych
Jeśli chcesz przeprowadzić własną analizę w Excelu, dashboard umożliwia wygenerowanie pełnego raportu w formacie `.csv`, który zawiera kompletną historię wszystkich 60 interakcji testowych.

## 🚀 Jak uruchomić?

1. **Sklonuj repozytorium:**
 * git clone [https://github.com/piotrwalas1/Banking_RAG_Project.git](https://github.com/piotrwalas1/Banking_RAG_Project.git)
   cd Banking_RAG_Project
 *  2. **Zainstaluj zależności:**
  * pip install pandas matplotlib numpy tabulate streamlit plotly python-dotenv
3. **Skonfiguruj środowisko:**
 *  Dodaj swoje klucze API dla modeli Gemini.
   4. **Uruchom analizę i wizualizację:**
   *   python ingest.py
   *   python bank_bot.py
  *    python test_runner.py
    *  streamlit run dashboard.py
