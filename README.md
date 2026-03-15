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
### 5. `dashboard_compare.py` (Analytical Dashboard)
* Wizualizacja wyników testów, porównywanie wyników (do wyciągania wniosków z testów A/B).

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

## 🧪 Testy A/B i Porównanie Technik Promptingu

Kluczowym elementem projektu była optymalizacja odpowiedzi modelu poprzez testy porównawcze różnych strategii promptingu. Przeprowadzono ewaluację na zbiorze **60 pytań testowych** dla trzech wariantów:

### Opis techniczny promptów:
* **V0 - Baseline (Standard):** Prosta instrukcja udzielenia odpowiedzi na podstawie kontekstu bez dodatkowych wytycznych logicznych. **Prompt:** "Jesteś ekspertem bankowym. Odpowiadaj konkretnie na podstawie dokumentów.\n\n"
* **V1 - Analytical Expert (CoT):** Wprowadzenie techniki *Chain-of-Thought*. Model został poinstruowany, aby najpierw zidentyfikować produkt, przejrzeć warunki, a dopiero potem sformułować odpowiedź. **Prompt:** "Jesteś ekspertem ds. analizy regulaminów bankowych Santander Bank Polska. 
Twoim zadaniem jest udzielenie precyzyjnej odpowiedzi na podstawie dostarczonego kontekstu.
Zastosuj metodę Chain-of-Thought:
1. IDENTYFIKACJA: Określ, o jaki produkt (np. Konto Select, karta Visa) i jaką czynność (np. przelew, wypłata) pyta klient.
2. ANALIZA WARUNKÓW: Przeszukaj kontekst pod kątem wyjątków, gwiazdek (*) i warunków zwalniających z opłaty (np. wpływ 2000 zł).
3. WYLICZENIE: Jeśli w tekście podanych jest kilka kwot, uzasadnij, dlaczego wybierasz konkretną.
4. ODPOWIEDŹ: Podaj ostateczną informację w sposób uprzejmy i konkretny.
Jeśli w kontekście brakuje informacji o konkretnym produkcie, napisz: "Przepraszam, ale dostarczone dokumenty nie zawierają informacji na temat [nazwa produktu]. Proszę o kontakt z infolinią". Nie zmyślaj danych."
* **V2 - Evidence-Based Auditor (CoT + Extraction):** Najbardziej rygorystyczna wersja. Model musi wypisać dosłowne cytaty z regulaminu przed udzieleniem końcowej odpowiedzi, co minimalizuje ryzyko halucynacji. **Prompt:** "Działasz jako system weryfikacji dokumentacji bankowej. Odpowiadaj wyłącznie na podstawie faktów.
Zanim sformułujesz odpowiedź, wykonaj wewnętrzną analizę krok po kroku:
Krok 1: Wypisz dosłowne cytaty z dostarczonego tekstu, które dotyczą pytania.
Krok 2: Sprawdź, czy cytaty nie zawierają wykluczeń (np. "nie dotyczy kont walutowych").
Krok 3: Porównaj pytanie z tabelą opłat i upewnij się, że jednostka (PLN, USD, %) jest poprawna.
Krok 4: Sformułuj odpowiedź końcową, usuwając techniczne notatki.
Twoja odpowiedź musi być bezpośrednia. Jeśli informacja jest niejednoznaczna, wskaż punkt w regulaminie, który budzi wątpliwości."

### Wyniki Benchmarkingu (A/B/C):

| Metryka | V0 (Baseline) | V1 (Analytical) | V2 (Evidence-Based) |
| :--- | :--- | :--- | :--- |
| **Średnia Ocena (1-5)** | 3.67 | 3.73 | **3.88** |
| **Hit Rate (Skuteczność)** | 98.33% | **100.0%** | **100.0%** |
| **Średnia Latencja** | **1.35s** | 1.77s | 2.27s |
| **Koszt (60 zapytań)** | **$0.164** | $0.174 | $0.188 |

 <p align="center">
  <img src="https://github.com/piotrwalas1/Banking_RAG_Project/blob/main/dashboardv0v1.png" width="600" title="raport1">
</p>

**Porównanie efektywności technik promptingu (V0 vs V1)**

 <p align="center">
  <img src="https://github.com/piotrwalas1/Banking_RAG_Project/blob/main/dashboardv0v2.png" width="600" title="raport1">
</p>

**Porównanie efektywności technik promptingu (V0 vs V2)**

### 3. Wnioski z optymalizacji:
- **Wzrost jakości:** Wersja **V2** poprawiła jakość odpowiedzi o **~6%** względem wersji bazowej (V0).
- **Bezpieczeństwo danych:** Zastosowanie rygorystycznego promptu w wersji V2 wyeliminowało halucynacje przy trudnych pytaniach o limity wiekowe i opłaty walutowe.
- **Koszt precyzji:** Wyższa jakość w wersji V2 wiąże się z ok. 40% wyższą latencją (z 1.35s do 2.27s), co w sektorze bankowym jest akceptowalnym kompromisem w zamian za poprawność merytoryczną.

---

## 📊 Dashboard i Analiza Wyników
Projekt zawiera narzędzie do porównywania raportów, które pozwala na:
- Wykrywanie regresji (sprawdzenie, na które pytania model odpowiedział gorzej po zmianie promptu).
- Eksport zestawień do plików CSV.
- Analizę korelacji między kosztem a jakością odpowiedzi.

## 🚀 Jak uruchomić?

1. **Sklonuj repozytorium:**
 * git clone [https://github.com/piotrwalas1/Banking_RAG_Project.git](https://github.com/piotrwalas1/Banking_RAG_Project.git)
   cd Banking_RAG_Project
 *   **2. Zainstaluj zależności:**
  * "pip install pandas matplotlib numpy tabulate streamlit plotly python-dotenv"
3. **Skonfiguruj środowisko:**
 *  Dodaj swoje klucze API dla modeli Gemini.
   4. **Uruchom analizę i wizualizację:**
   *   python ingest.py
   *   python bank_bot.py
  *    python test_runner.py
    *  streamlit run dashboard.py
