# day3.py - loops and continue

def rate_response(response):
    score = 0
    if len(response) > 100: score +=2
    elif len(response) > 50: score +=1
    if len(response.split()) > 15: score +=2
    if "?" in response: score +=1
    if score >=4: return "Excellent",score
    elif score >=2: return "Average",score
    else: return "Rejected",score
    

response = [
    "ML is AI",
    "Machine learning is AI where computers learn patterns from data automatically",
    "RLHF trains LLMs using human feedback - exactly what I do at Ethara AI daily"
]

for i,r in enumerate(response):
    rating, score = rate_response(r)
    print(f"Response {i+1} [{score}/5]: {rating}")    