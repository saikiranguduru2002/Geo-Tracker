from groq import Groq
import os
from dotenv import load_dotenv
from prompts import get_queries

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(query):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content

def check_visibility(brand, category):
    queries = get_queries(category)
    results = []

    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        answer = ask_ai(query)
        mentioned = brand.lower() in answer.lower()

        if mentioned:
            print(f"✅ '{brand}' was mentioned")
        else:
            print(f"❌ '{brand}' was NOT mentioned")
        print()

        results.append({
            "query": query,
            "answer": answer,
            "mentioned": mentioned
        })

    return results

def calculate_score(results):
    total = len(results)
    mentions = sum(1 for r in results if r["mentioned"])
    score = round((mentions / total) * 100)
    return score, mentions, total