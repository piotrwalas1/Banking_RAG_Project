import os
import json
import time
from langchain_google_vertexai import ChatVertexAI
from bank_bot import get_rag_chain, invoke_with_metrics

# ---Uwaga!!! KONFIGURACJA wpisz Twoj project id---
PROJECT_ID = "Tu wpisz project id"
LOCATION = "us-central1"
INPUT_FILE = "test_cases.json"
OUTPUT_FILE = "advanced_report.json"

# --- CENNIK PRO Przykładowy---
COST_INPUT_1K = 0.00125  
COST_OUTPUT_1K = 0.00375 

def run_advanced_evaluation():
    print("\n🚀 START: EVALUATION BENCHMARK - MODEL: PRO")
    
    try:
        bot_chain = get_rag_chain()
    
        judge_llm = ChatVertexAI(
            model_name="gemini-2.5-pro", 
            project=PROJECT_ID,
            location=LOCATION,
            temperature=0
        )
        print("✅ Systemy załadowane. Sędzia klasy PRO gotowy.")
    except Exception as e:
        print(f"❌ Błąd inicjalizacji: {e}")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Brak pliku: {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []
    stats = {"latency": 0, "hits": 0, "score_sum": 0, "cost_sum": 0, "count": len(test_cases)}

    for i, case in enumerate(test_cases):
        case_id = case.get('id', i+1)
        query = case.get('prompt') or case.get('question')
        expected = case.get('expected_behavior') or case.get('expected_answer')

        print(f"🔄 [{i+1}/{len(test_cases)}] ID: {case_id}", end=" | ", flush=True)

        try:
            res = invoke_with_metrics(bot_chain, query)
            
            judge_prompt = f"Oceń odpowiedź (1-5) pod kątem merytorycznym.\nPytanie: {query}\nOczekiwana: {expected}\nBot: {res['answer']}\nZwróć TYLKO cyfrę."
            
            score_out = judge_llm.invoke(judge_prompt).content.strip()
            score = int(''.join(filter(str.isdigit, score_out)) or 1)

            is_hit = "nie mam informacji" not in res['answer'].lower() and len(res['answer']) > 20
            
            tokens_in = (len(query) + 8000) / 4
            tokens_out = len(res['answer']) / 4
            query_cost = ((tokens_in / 1000) * COST_INPUT_1K) + ((tokens_out / 1000) * COST_OUTPUT_1K)

            stats["latency"] += res["latency"]
            stats["score_sum"] += score
            stats["cost_sum"] += query_cost
            if is_hit: stats["hits"] += 1

            results.append({
                "id": case_id, "query": query, "score": score, 
                "latency": res["latency"], "is_hit": is_hit, "cost_usd": round(query_cost, 6)
            })
            print(f"Ocena: {score}/5")
            time.sleep(1) 

        except Exception as e:
            print(f"⚠️ Błąd: {e}")

    summary = {
        "avg_relevance_score": round(stats["score_sum"] / stats["count"], 2),
        "avg_latency_sec": round(stats["latency"] / stats["count"], 3),
        "hit_rate_percent": round((stats["hits"] / stats["count"]) * 100, 2),
        "total_audit_cost_usd": round(stats["cost_sum"], 5)
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "details": results}, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ GOTOWE! Raport: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_advanced_evaluation()