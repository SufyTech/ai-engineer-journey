# day4 - functions 

def clean_input(text):
    return text.strip()

def build_prompt(question, context=""):
    if context:
        return f"Context: {context}\nQuestion: {question}"
    return f"Question: {question}"

def rate_response(response, min_words=10):
    words = len(response.split())
    if words >= min_words and len(response) > 50:
        return 5
    elif words >= 5:
        return 3
    return 1

def is_safe(response):
    bad_words= ["hate", "violence", "illegal"]
    return not any(w in response.lower() for w in bad_words)

def format_result(question, answer, score):
    return f"Q:{question}\nA: {answer}\nScore: {score}/5\nSafe: {is_safe(answer)}"

q = "What is deep learning?"
a = "Deep learning uses neural networks with many layers to learn complex patterns from large data automatically."
print(format_result(clean_input(q), a , rate_response(a)))
