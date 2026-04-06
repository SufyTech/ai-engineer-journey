# day8.py - Groq API - FREE - 6 April 2026
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(question, system="You are helpful"):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Test 1
print(ask_ai("What is RLHF in 2 sentences?"))

# Test 2
print(ask_ai(
    "I do RLHF at an AI company. What makes a perfect response?",
    "You are a senior AI researcher"
))