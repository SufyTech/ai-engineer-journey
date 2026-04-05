import json

def save_ratings(ratings, file="ratings.json"):
    with open(file, "w") as f:
        json.dump(ratings, f, indent=2)
    print(f"Saved {len(ratings)} ratings!")
    
def load_ratings(file="ratings.json"):
    try:
        with open(file,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def build_rag_prompt(question, context):
    return f"""Answer using ONLY the context below.

CONTEXT:{context}
QUESTION: {question}
ANSWER:"""

ratings = [
    {"prompt": "Explain RLHF", "score":5, "note": "Perfect"},
    {"prompt":"Write poem", "score":2, "note":"Too short"},
]

save_ratings(ratings)
loaded = load_ratings()
for r in loaded:
    print(f"Score {r['score']}/5-{r['prompt']}")


prompt = build_rag_prompt("What is RLHF?","ELHF uses human feedback to train LLMs")
print(f"\nGenerated prompt:\n{prompt}")